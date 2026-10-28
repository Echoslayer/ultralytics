from ultralytics import YOLO

model = YOLO("yolo26n.pt")
results = model("https://ultralytics.com/images/bus.jpg", save=True)

# Audit inspection, appended after the unchanged tutorial example.
from pathlib import Path
print('AUDIT', type(results).__name__, len(results), type(results[0]).__name__)
print('BOXES', results[0].boxes.shape)
print('SAVED', Path(results[0].save_dir, 'bus.jpg').is_file(), results[0].save_dir)
