import json
import subprocess
import sys
import time
from pathlib import Path


if __name__ == "__main__":
    root = Path.cwd()
    out = Path(sys.argv[1]).resolve()
    if len(sys.argv) == 2:
        out.mkdir(parents=True, exist_ok=False)
        steps = []
        for mode in ("train", "reload"):
            start = time.perf_counter()
            with (out / f"{mode}.log").open("w", encoding="utf-8") as log:
                p = subprocess.run([sys.executable, __file__, str(out), mode], stdout=log, stderr=subprocess.STDOUT)
            steps.append({"mode": mode, "exit": p.returncode, "seconds": time.perf_counter() - start})
            (out / "execution.json").write_text(json.dumps(steps, indent=2))
            assert p.returncode == 0, f"See {out / (mode + '.log')}"
        print(json.dumps(steps, indent=2))
    else:
        from ultralytics import YOLO

        if sys.argv[2] == "train":
            model = YOLO(root / "yolo26n.pt")
            metrics = model.train(data="coco8.yaml", epochs=1, imgsz=640, device="cpu", project=str(out), name="train")
            for name in ("best", "last"):
                assert (out / "train/weights" / f"{name}.pt").stat().st_size > 0
            (out / "metrics.json").write_text(json.dumps(metrics.results_dict, indent=2))
        else:
            summary = {}
            for name in ("best", "last"):
                model = YOLO(out / "train/weights" / f"{name}.pt")
                result = model(root / "bus.jpg", device="cpu", save=True, project=str(out), name=f"reload-{name}")[0]
                assert result.orig_shape == (1080, 810)
                assert result.boxes is not None
                assert (Path(result.save_dir) / "bus.jpg").exists()
                summary[name] = {"boxes": len(result.boxes), "detections": result.summary()}
            (out / "reload.json").write_text(json.dumps(summary, indent=2))
