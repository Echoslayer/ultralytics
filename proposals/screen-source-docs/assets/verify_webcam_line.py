"""Run the fixed usage/python.md webcam line against a fake camera, since no real camera was used."""

import sys
from pathlib import Path

import cv2

sys.path.insert(0, str(Path(__file__).parent))
from probe_mem import FakeCam  # noqa: E402

from ultralytics import YOLO  # noqa: E402

cv2.VideoCapture = FakeCam
model = YOLO("yolo26n.pt")
results = model.predict(source="0", stream=True)  # a webcam never ends on its own, so iterate this generator
print("predict returned:", type(results).__name__, flush=True)
for i, r in enumerate(results):
    if i == 2:
        break
print("frames read:", i + 1, "shape:", r.orig_shape)
results.close()
