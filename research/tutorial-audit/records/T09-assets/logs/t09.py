import hashlib
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path


if __name__ == "__main__":
    out = Path(sys.argv[1]).resolve()
    if len(sys.argv) == 2:
        out.mkdir(parents=True, exist_ok=False)
        timings = {}
        for stage in ("export", "predict"):
            start = time.perf_counter()
            with (out / f"{stage}.log").open("w", encoding="utf-8") as log:
                process = subprocess.run([sys.executable, __file__, str(out), stage], stdout=log, stderr=subprocess.STDOUT)
            timings[stage] = {"exit_code": process.returncode, "seconds": time.perf_counter() - start}
            (out / "execution.json").write_text(json.dumps(timings, indent=2))
            assert process.returncode == 0, out / f"{stage}.log"
    else:
        from ultralytics import YOLO

        if sys.argv[2] == "export":
            shutil.copy2("yolo26n.pt", out / "yolo26n.pt")
            exported = Path(YOLO(out / "yolo26n.pt").export(format="onnx", device="cpu", imgsz=640))
            assert exported == out / "yolo26n.onnx" and exported.stat().st_size > 0
        else:
            import numpy as np
            import onnx
            import onnxruntime as ort

            graph = onnx.load(out / "yolo26n.onnx")
            onnx.checker.check_model(graph)
            report = {"opset": [(v.domain, v.version) for v in graph.opset_import], "models": {}}
            for name, suffix in [("pytorch", "pt"), ("onnx", "onnx")]:
                model = YOLO(out / f"yolo26n.{suffix}", task="detect")
                result = model.predict("bus.jpg", imgsz=640, rect=False, conf=0.25, iou=0.7,
                                       nms=None, device="cpu", save=True, project=str(out), name=name)[0]
                report["models"][name] = {"boxes": result.boxes.data.tolist(), "shape": list(result.orig_shape)}
                assert (out / name / "bus.jpg").exists()
            # shortcut: one image and equal class/order check; use dataset-level matching for quality claims.
            pt = np.array(report["models"]["pytorch"]["boxes"])
            exported = np.array(report["models"]["onnx"]["boxes"])
            assert pt.shape == exported.shape and len(pt) > 0
            assert np.array_equal(pt[:, 5], exported[:, 5])
            report["max_coordinate_difference_pixels"] = float(np.max(np.abs(pt[:, :4] - exported[:, :4])))
            report["max_confidence_difference"] = float(np.max(np.abs(pt[:, 4] - exported[:, 4])))
            assert report["max_coordinate_difference_pixels"] < 1
            assert report["max_confidence_difference"] < 0.001
            session = ort.InferenceSession(str(out / "yolo26n.onnx"), providers=["CPUExecutionProvider"])
            report["onnx_input"] = [{"name": x.name, "shape": x.shape, "type": x.type} for x in session.get_inputs()]
            report["onnx_output"] = [{"name": x.name, "shape": x.shape, "type": x.type} for x in session.get_outputs()]
            report["providers"] = session.get_providers()
            report["files"] = {f.name: {"bytes": f.stat().st_size, "sha256": hashlib.sha256(f.read_bytes()).hexdigest()}
                               for f in (out / "yolo26n.pt", out / "yolo26n.onnx")}
            (out / "results.json").write_text(json.dumps(report, indent=2))
