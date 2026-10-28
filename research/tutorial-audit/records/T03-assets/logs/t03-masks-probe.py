from pathlib import Path
from ultralytics import YOLO
result = YOLO(Path.cwd() / "yolo26n.pt").predict(source=Path.cwd() / "bus.jpg", device="cpu")[0]
print("Detection masks:", result.masks, flush=True)
result.masks.data
