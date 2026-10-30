"""T12b: do real predictions ever yield an empty masks.xy contour (which crashes the guide's drawContours)?"""

from pathlib import Path

from ultralytics import YOLO
from ultralytics.utils import ASSETS

HERE = Path(__file__).parent
model = YOLO(str(HERE / "yolo26n-seg.pt"))
for src in [ASSETS / "bus.jpg", ASSETS / "zidane.jpg", HERE / "boats.jpg"]:
    for imgsz in (160, 320, 640):
        for retina in (False, True):
            r = model.predict(str(src), conf=0.01, imgsz=imgsz, retina_masks=retina, max_det=300, verbose=False)[0]
            empty = [i for i, xy in enumerate(r.masks.xy) if len(xy) == 0] if r.masks is not None else []
            tiny = [i for i, xy in enumerate(r.masks.xy) if 0 < len(xy) < 3] if r.masks is not None else []
            print(f"{src.stem:<7} imgsz={imgsz:<4} retina={retina!s:<5} dets={len(r):4d} empty_xy={len(empty):3d} pts<3={len(tiny):3d}")
