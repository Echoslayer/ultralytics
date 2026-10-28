import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time


if __name__ == "__main__":
    root = Path.cwd()
    out = Path(sys.argv[1]).resolve()
    if len(sys.argv) == 2:
        out.mkdir()
        shutil.copy2(root / "yolo26n.pt", out)
        shutil.copy2(root / "bus.jpg", out)
        import importlib.util
        package = Path(importlib.util.find_spec("ultralytics").origin).parent
        shutil.copy2(package / "assets/zidane.jpg", out)
        config = out / "config/Ultralytics"
        config.mkdir(parents=True)
        settings = json.loads((root / "config/Ultralytics/settings.json").read_text())
        settings.update(runs_dir=str(out / "runs"), tensorboard=False, wandb=False)
        (config / "settings.json").write_text(json.dumps(settings))
        env = dict(os.environ, YOLO_CONFIG_DIR=str(out / "config"), YOLO_AUTOINSTALL="False")
        yolo = str(Path(sys.executable).with_name("yolo.exe"))
        commands = {
            "02": [sys.executable, "-c", "import ultralytics; ultralytics.checks()"],
            "04": [yolo, "predict", "model=yolo26n.pt", "source=zidane.jpg", "device=cpu", "name=cell04"],
            "08": [yolo, "val", "model=yolo26n.pt", "data=coco8.yaml", "device=cpu", "workers=0", "name=cell08"],
            "11": [yolo, "train", "model=yolo26n.pt", "data=coco8.yaml", "epochs=3", "imgsz=640", "device=cpu", "workers=0", "name=cell11"],
            "13": [yolo, "export", "model=yolo26n.pt", "format=torchscript", "device=cpu"],
            "15": [sys.executable, __file__, str(out), "python"],
        }
        execution = {}
        for cell, command in commands.items():
            start = time.perf_counter()
            with (out / f"cell{cell}.log").open("w", encoding="utf-8") as log:
                result = subprocess.run(command, cwd=out, env=env, stdout=log, stderr=subprocess.STDOUT)
            execution[cell] = dict(command=command, exit_code=result.returncode, seconds=time.perf_counter()-start)
            (out / "execution.json").write_text(json.dumps(execution, indent=2))
            assert result.returncode == 0, out / f"cell{cell}.log"
        assert (out / "yolo26n.torchscript").stat().st_size > 0
        assert (out / "runs/detect/cell11/weights/best.pt").is_file()
    else:
        from ultralytics import YOLO

        model = YOLO("yolo26n.yaml")
        model = YOLO("yolo26n.pt")
        model.train(data="coco8.yaml", epochs=3, device="cpu", workers=0, project=str(out / "python"), name="train")
        metrics = model.val(device="cpu", workers=0, project=str(out / "python"), name="val")
        results = model("bus.jpg", device="cpu", save=True, project=str(out / "python"), name="predict")
        export = model.export(format="onnx", device="cpu")
        reloaded = YOLO(export, task="detect")("bus.jpg", device="cpu")
        scripted = YOLO(str(out / "yolo26n.torchscript"), task="detect")("zidane.jpg", device="cpu")
        summary = dict(metrics=metrics.results_dict, boxes=results[0].boxes.data.tolist(),
                       onnx_boxes=reloaded[0].boxes.data.tolist(), torchscript_boxes=scripted[0].boxes.data.tolist(),
                       export=str(export))
        (out / "summary.json").write_text(json.dumps(summary, indent=2))
        assert len(results) == len(reloaded) == len(scripted) == 1
        assert len(results[0].boxes) == len(reloaded[0].boxes) > 0
        assert Path(export).stat().st_size > 0
