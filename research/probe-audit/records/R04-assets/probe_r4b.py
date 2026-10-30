"""R04 follow-up: is the static-ONNX val gap explained by rect alone? Prints only."""
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1])
OUT = Path(sys.argv[2]).resolve()
from ultralytics import YOLO

for imgsz in (320, 640):
    files = {"pt": "yolo26n.pt"}
    for tag, kw in (("static", {}), ("dynamic", {"dynamic": True})):
        f = Path(YOLO("yolo26n.pt").export(format="onnx", imgsz=imgsz, **kw))
        files[tag] = str(f.replace(OUT / f"b_{imgsz}_{tag}.onnx"))
    for tag, f in files.items():
        for rect in (True, False):
            v = YOLO(f).val(data="coco8.yaml", imgsz=imgsz, batch=4, rect=rect, plots=False, verbose=False,
                            project=str(OUT), name=f"b{imgsz}{tag}{rect}")
            print(f"imgsz={imgsz} {tag:8} rect={rect!s:5} -> effective rect={v.speed and None} map50-95={v.box.map:.4f} map50={v.box.map50:.4f}")
