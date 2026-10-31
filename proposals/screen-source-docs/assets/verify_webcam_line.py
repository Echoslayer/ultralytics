"""Run the webcam lines from usage/python.md as written against a fake camera, since no real camera was used."""

import re
import sys
import textwrap
from pathlib import Path

import cv2

sys.path.insert(0, str(Path(__file__).parent))
from probe_mem import FakeCam  # noqa: E402

from ultralytics import YOLO  # noqa: E402

text = Path(sys.argv[1]).read_text(encoding="utf-8")
code = textwrap.dedent(re.search(r'^ +for result in model\.predict\(source="0".*?\n.*?\n', text, re.M).group(0))
print(code)
calls = []
real = FakeCam.read


def read(self):
    calls.append(1)
    return real(self)


FakeCam.read = read
cv2.VideoCapture = FakeCam
model = YOLO("yolo26n.pt")
exec(code)
print("frames read:", len(calls), "result shape:", result.orig_shape)
