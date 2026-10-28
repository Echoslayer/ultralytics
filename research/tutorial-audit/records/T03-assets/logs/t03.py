import json
import sys
from pathlib import Path
import numpy as np
import torch
import ultralytics
from ultralytics import YOLO

root = Path.cwd()
out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=False)
model = YOLO(root / "yolo26n.pt")
results = model.predict(source=root / "bus.jpg", device="cpu", conf=0.25)
assert isinstance(results, list) and len(results) == 1
result = results[0]
boxes = result.boxes
assert boxes is not None
xyxy = boxes.xyxy.cpu().numpy()
h, w = result.orig_shape
np.testing.assert_allclose(boxes.xyxyn.cpu(), xyxy / [w, h, w, h], atol=1e-6)
np.testing.assert_allclose(boxes.xywhn.cpu(), boxes.xywh.cpu().numpy() / [w, h, w, h], atol=1e-6)
converted = result.cpu().numpy()
np.testing.assert_array_equal(converted.boxes.data, boxes.data.cpu().numpy())
rows = [
    {"row": i, "class_id": int(cls), "name": result.names[int(cls)], "confidence": float(conf),
     "xyxy": coords.tolist(), "xywh": boxes.xywh[i].tolist(), "xyxyn": boxes.xyxyn[i].tolist(),
     "xywhn": boxes.xywhn[i].tolist()}
    for i, (coords, cls, conf) in enumerate(zip(xyxy, boxes.cls.tolist(), boxes.conf.tolist()))
]
result.save(filename=str(out / "bus.jpg"))
result.save_txt(str(out / "bus.txt"), save_conf=True)
summary = {"python": sys.version, "ultralytics": ultralytics.__version__, "torch": torch.__version__,
           "package_path": ultralytics.__file__, "result_type": type(result).__name__,
           "orig_shape": list(result.orig_shape), "boxes_shape": list(boxes.data.shape),
           "masks": result.masks, "probs": result.probs, "numpy_type": type(converted.boxes.data).__name__,
           "rows": rows}
(out / "results.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
print(json.dumps(summary, indent=2))
print("PASS: normalized coordinates and CPU/NumPy conversion")
