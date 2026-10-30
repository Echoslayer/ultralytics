import sys, numpy as np
sys.path.insert(0, sys.argv[1])
import ultralytics
from ultralytics import YOLO
m = YOLO("yolo26n.pt").val(data="coco8.yaml", imgsz=640, batch=8, workers=0, plots=False, verbose=False, project=sys.argv[2])
b = m.box
idx = list(b.ap_class_index)
fill = np.delete(b.maps, idx)
print("ultralytics", ultralytics.__version__, ultralytics.__file__)
print("nc", b.nc, "evaluated", len(idx), idx)
print("overall map", b.map, "filler unique", np.unique(fill))
assert len(idx) < b.nc and np.allclose(fill, b.map)
assert np.allclose(b.maps[idx], b.ap)
print("OK: filler == overall mAP; evaluated entries == per-class AP")
