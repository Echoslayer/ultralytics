def benchmark(
    model=WEIGHTS_DIR / "yolo26n.pt",
    data=None,
    imgsz=160,
    quantize=None,
    device="cpu",
    verbose=False,
    eps=1e-3,
    format="",
    **kwargs,
):
    """Benchmark a YOLO model across different formats for speed and accuracy.

    Args:
        model (str | Path | YOLO): Path to the model file or directory, or a loaded YOLO model instance.
        data (str | None): Dataset to evaluate on, inherited from TASK2DATA if not passed.
        imgsz (int | list[int]): Square image size for the benchmark.
        quantize (int | str | None): Requested precision: 16 (FP16), 8 (INT8), or None/32 (FP32). Exported rows apply it
            at export, where a format may reject an explicit 32 or fall back to the precision it requires; the native
            PyTorch row is not exported and only 16 affects it, selecting FP16 inference off CPU. Each format then runs
            inference at its own runtime precision.
        device (str): Device to run the benchmark on, e.g. 'cpu', 'cuda:0' or 'mps'.
        verbose (bool | float): If True or a float, raise on non-assertion benchmark failures; a float also asserts that
            every successful format's metric exceeds this floor value.
        eps (float): Epsilon value for divide by zero prevention.
        format (str): Export format for benchmarking. If not supplied, all formats are benchmarked.
        **kwargs (Any): Export options; nms selects the same head for native and exported benchmarks.

    Returns:
        (polars.DataFrame): A Polars DataFrame of string-formatted benchmark results for each format, including status,
            file size, metric, inference time, and FPS.

    Examples:
        Benchmark a YOLO model with default settings:
        >>> from ultralytics.utils.benchmarks import benchmark
        >>> benchmark(model="yolo26n.pt", imgsz=640)
    """
    from ultralytics.cfg import _handle_deprecation

    quantize = _handle_deprecation(kwargs).pop("quantize", quantize)  # updates kwargs in place, half/int8 -> quantize
    imgsz = check_imgsz(imgsz)
    assert imgsz[0] == imgsz[1] if isinstance(imgsz, list) else True, "benchmark() only supports square imgsz."

    import polars as pl  # scope for faster 'import ultralytics'

    pl.Config.set_tbl_cols(-1)  # Show all columns
    pl.Config.set_tbl_rows(-1)  # Show all rows
    pl.Config.set_tbl_width_chars(-1)  # No width limit
    pl.Config.set_tbl_hide_column_data_types(True)  # Hide data types
    pl.Config.set_tbl_hide_dataframe_shape(True)  # Hide shape info
    pl.Config.set_tbl_formatting("ASCII_BORDERS_ONLY_CONDENSED")

    device = select_device(device, verbose=False)
    if isinstance(model, (str, Path)):
        model = YOLO(model)
    data = data or TASK2DATA[model.task]  # task to dataset, i.e. coco8.yaml for task=detect
    key = TASK2METRIC[model.task]  # task to metric, i.e. metrics/mAP50-95(B) for task=detect
    if isinstance(model, (YOLOE, YOLOWorld)) and not hasattr(model.model.model[-1], "lrpc"):
        data = convert_ndjson_to_yolo_if_needed(data, split="val")
        names = [name.split("/", 1)[0] for name in check_det_dataset(data)["names"].values()]
        # exports bake the current vocabulary, while validation re-prompts YOLOE always and YOLO-World on new names
        if isinstance(model, YOLOE) or list(model.names.values()) != names:
            model = deepcopy(model, {id(model.predictor): None, id(model.trainer): None})
            model.set_classes(names, model.get_text_pe(names)) if isinstance(model, YOLOE) else model.set_classes(names)

    y = []
    t0 = time.time()

    format_arg = format.lower()
    if format_arg:
        formats = frozenset(export_formats()["Argument"])
        assert format_arg in formats, f"Expected format to be one of {formats}, but got '{format_arg}'."
    for name, export_format, suffix, cpu, gpu, valid_args, _ in zip(*export_formats().values()):
        emoji, filename = "❌", None  # export defaults
        try:
            if format_arg and format_arg != export_format:
                continue
            if IS_PYTHON_MINIMUM_3_13 and not format_arg and export_format in {"saved_model", "pb", "edgetpu"}:
                continue

            # Checks
            if export_format == "pb":
                assert model.task != "obb", "TensorFlow GraphDef not supported for OBB task"
            elif export_format == "edgetpu":
                assert LINUX and not ARM64, "Edge TPU export only supported on non-aarch64 Linux"
                assert shutil.which("edgetpu_compiler"), "Edge TPU benchmark requires edgetpu_compiler"
            elif export_format == "coreml":
                assert MACOS or (LINUX and not ARM64), "CoreML export only supported on macOS and non-aarch64 Linux"
                # coremltools deadlocks after OpenVINO on macOS Python 3.13 (conflicting OpenMP runtimes); CoreML
                # is still benchmarked on non-aarch64 Linux Python 3.13.
                assert not (MACOS and IS_PYTHON_MINIMUM_3_13), (
                    "CoreML not benchmarked on macOS Python>=3.13 (coremltools/OpenVINO OpenMP deadlock)"
                )
            if export_format in {"saved_model", "pb", "edgetpu"}:
                assert not isinstance(model, YOLOWorld), "YOLOWorldv2 TensorFlow exports not supported by onnx2tf yet"
            if export_format == "paddle":
                assert not isinstance(model, YOLOWorld), "YOLOWorldv2 Paddle exports not supported yet"
                assert (LINUX and not IS_JETSON) or MACOS, "Windows and Jetson Paddle exports not supported yet"
                # PaddlePaddle export works standalone on Python 3.13 but its native protobuf clashes with the
                # protobuf>=6.31.1 that TensorFlow loads earlier in this shared benchmark process, causing a segfault.
                assert not IS_PYTHON_MINIMUM_3_13, (
                    "PaddlePaddle not benchmarked on Python>=3.13 (protobuf ABI conflict with TensorFlow)"
                )
            if export_format == "mnn":
                assert not isinstance(model, YOLOWorld), "YOLOWorldv2 MNN exports not supported yet"
                # MNN export works standalone on Python 3.13 but its ONNX-parsing protobuf clashes with the
                # protobuf>=6.31.1 that TensorFlow loads earlier in this shared benchmark process, aborting the run.
                assert not IS_PYTHON_MINIMUM_3_13, (
                    "MNN not benchmarked on Python>=3.13 (protobuf ABI conflict with TensorFlow)"
                )
            if export_format == "ncnn":
                assert not isinstance(model, YOLOWorld), "YOLOWorldv2 NCNN exports not supported yet"
            if export_format == "imx":
                assert not isinstance(model, YOLOWorld), "YOLOWorldv2 IMX exports not supported"
                assert model.task in {"detect", "classify", "pose", "segment"}, (
                    "IMX export is only supported for detection, classification, pose estimation and segmentation tasks"
                )
                assert "C2f" in model.__str__(), "IMX only supported for YOLOv8n and YOLO11n"
            if export_format == "rknn":
                assert not isinstance(model, YOLOWorld), "YOLOWorldv2 RKNN exports not supported yet"
                assert LINUX, "RKNN only supported on Linux"
                assert not is_rockchip(), "RKNN Inference only supported on Rockchip devices"
            if export_format == "executorch":
                assert not isinstance(model, YOLOWorld), "YOLOWorldv2 ExecuTorch exports not supported yet"
            if export_format == "axelera":
                assert not isinstance(model, YOLOWorld), "YOLOWorldv2 Axelera exports not supported"
                assert LINUX and not (ARM64 and IS_DOCKER), (
                    "export is only supported on Linux and is not supported on ARM64 Docker."
                )
            if export_format == "xilinx":
                assert LINUX, "AMD Xilinx export only supported on Linux"
                assert find_spec("quark"), "AMD Xilinx benchmark requires amd-quark"
            if export_format == "litert":
                assert MACOS or (LINUX and not ARM64), "LiteRT benchmark only supported on Linux x86 and macOS"
                # benchmark() deadlocks on the ai-edge-litert/TensorFlow abseil mutex (RAW: Lock blocking) on macOS CI
                # when litert runs after other TF-based formats in the shared process; still benchmarked locally.
                assert not (MACOS and is_github_action_running()), (
                    "LiteRT not benchmarked on macOS CI (ai-edge-litert/TF abseil mutex deadlock)"
                )
            if "cpu" in device.type:
                assert cpu, "inference not supported on CPU"
            if "cuda" in device.type:
                assert gpu, "inference not supported on GPU"

            # Export
            if export_format == "-":
                filename = model.pt_path or model.ckpt_path or model.model_name
                exported_model = deepcopy(model, {id(model.predictor): None, id(model.trainer): None})  # PyTorch format
            else:
                export_data = data if "data" in valid_args else None
                filename = model.export(
                    imgsz=imgsz,
                    format=export_format,
                    quantize=quantize,
                    data=export_data,
                    device=device,
                    verbose=False,
                    **kwargs,
                )
                exported_model = RTDETR(filename) if isinstance(model, RTDETR) else YOLO(filename, task=model.task)
                assert suffix in str(filename), "export failed"
            emoji = "❎"  # indicates export succeeded

            # Predict
            assert model.task != "pose" or export_format != "pb", "GraphDef Pose inference is not supported"
            assert export_format != "edgetpu", "inference not supported"
            assert export_format != "coreml" or platform.system() == "Darwin", "inference requires macOS>=10.13"
            assert export_format != "coreai" or MACOS, "inference requires macOS"
            assert export_format != "axelera", "inference only supported on Axelera hardware"
            exported_model.predict(
                ASSETS / "bus.jpg",
                imgsz=imgsz,
                device=device,
                quantize=quantize,
                nms=kwargs.get("nms"),
                verbose=False,
            )

            # Validate
            results = exported_model.val(
                data=data,
                batch=1,
                imgsz=imgsz,
                rect=False,
                plots=False,
                device=device,
                quantize=quantize,
                nms=kwargs.get("nms"),
                verbose=False,
                conf=0.001,  # all the pre-set benchmark mAP values are based on conf=0.001
            )
            metric, speed = results.results_dict[key], results.speed["inference"]
            fps = round(1000 / (speed + eps), 2)  # frames per second
            y.append([name, "✅", round(file_size(filename), 1), round(metric, 4), round(speed, 2), fps])
        except Exception as e:
            if verbose:
                assert type(e) is AssertionError, f"Benchmark failure for {name}: {e}"
            LOGGER.error(f"Benchmark failure for {name}: {e}")
            y.append([name, emoji, round(file_size(filename), 1), None, None, None])  # mAP, t_inference

    # Print results
    check_yolo(device=device)  # print system info
    df = pl.DataFrame(y, schema=["Format", "Status❔", "Size (MB)", key, "Inference time (ms/im)", "FPS"], orient="row")
    df = df.with_row_index(" ", offset=1)  # add index info
    df_display = df.with_columns(pl.all().cast(pl.String).fill_null("-"))

    name = model.model_name
    dt = time.time() - t0
    legend = "Benchmarks legend:  - ✅ Success  - ❎ Export passed but validation failed  - ❌️ Export failed"
    s = f"\nBenchmarks complete for {name} on {data} at imgsz={imgsz} ({dt:.2f}s)\n{legend}\n{df_display}\n"
    LOGGER.info(s)
    with open("benchmarks.log", "a", errors="ignore", encoding="utf-8") as f:
        f.write(s)

    if verbose and isinstance(verbose, float):
        metrics = df[key].to_numpy()  # values to compare to floor
        floor = verbose  # minimum metric floor to pass, i.e. = 0.29 mAP for YOLOv5n
        assert all(x > floor for x in metrics if not np.isnan(x)), f"Benchmark failure: metric(s) < floor {floor}"

    return df_display
