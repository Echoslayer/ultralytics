import sys

import numpy as np

import ultralytics
from ultralytics import YOLO

assert ultralytics.__file__.startswith(sys.argv[1]), ultralytics.__file__
cases = [
    ("yolo26n.pt", "coco8.yaml", ["box"]),
    ("yolo26n-seg.pt", "coco8-seg.yaml", ["box", "seg"]),
    ("yolo26n-pose.pt", "coco8-pose.yaml", ["box", "pose"]),
    ("yolo26n-obb.pt", "dota8.yaml", ["box"]),
]
for w, d, keys in cases:
    m = YOLO(w).val(data=d, imgsz=640, batch=4, plots=False, verbose=False, project=sys.argv[2])
    for k in keys:
        r = getattr(m, k)
        idx = list(r.ap_class_index)
        rest = [c for c in range(len(r.maps)) if c not in idx]
        assert np.allclose(r.maps[idx], r.ap), (w, k)
        assert np.allclose(r.maps[rest], r.map), (w, k)
        print(f"{w} {k}: nc={len(r.maps)} evaluated={len(idx)} filler={len(rest)} map={r.map:.3f}")
