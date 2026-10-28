import json
import subprocess
import sys
import time
from pathlib import Path


if __name__ == "__main__":
    out = Path(sys.argv[1]).resolve()
    if len(sys.argv) == 2:
        out.mkdir(parents=True, exist_ok=False)
        start = time.perf_counter()
        with (out / "val.log").open("w", encoding="utf-8") as log:
            p = subprocess.run([sys.executable, __file__, str(out), "val"], stdout=log, stderr=subprocess.STDOUT)
        report = {"exit": p.returncode, "seconds": time.perf_counter() - start}
        (out / "execution.json").write_text(json.dumps(report, indent=2))
        assert p.returncode == 0, f"See {out / 'val.log'}"
        print(report)
    else:
        from ultralytics import YOLO

        model = YOLO(Path.cwd() / "t06-online/train/weights/best.pt")
        metrics = model.val(device="cpu", project=str(out), name="val")
        report = {
            "metrics": metrics.results_dict,
            "map75": metrics.box.map75,
            "maps": metrics.box.maps.tolist(),
            "evaluated_class_ids": metrics.box.ap_class_index.tolist(),
            "image_metrics": metrics.box.image_metrics,
            "remembered": {k: model.overrides.get(k) for k in ("data", "imgsz")},
        }
        assert len(report["image_metrics"]) == 4
        assert len(report["maps"]) == 80
        assert (out / "val/val_batch0_pred.jpg").exists()
        (out / "results.json").write_text(json.dumps(report, indent=2, default=lambda x: x.item()))
