"""Check the new sentence in simple-utilities.md against convert_segment_masks_to_yolo_seg on real PNG masks."""

import sys
import tempfile
from pathlib import Path

import cv2
import numpy as np

import ultralytics
from ultralytics.data.converter import convert_segment_masks_to_yolo_seg as convert

print(f"ultralytics {ultralytics.__version__} python {sys.version.split()[0]}")


def run(name, values, classes):
    """Write a mask with one square per pixel value, convert it, and return the class id of each output row."""
    with tempfile.TemporaryDirectory() as d:
        masks, out = Path(d, "masks"), Path(d, "labels")
        masks.mkdir()
        mask = np.zeros((64, 64), np.uint8)
        for i, v in enumerate(values):
            mask[8 + i * 20 : 20 + i * 20, 8:40] = v
        cv2.imwrite(str(masks / "a.png"), mask)
        convert(masks_dir=str(masks), output_dir=str(out), classes=classes)
        rows = (out / "a.txt").read_text().splitlines()
    ids = [int(r.split()[0]) for r in rows]
    print(f"{name}: pixel values {values}, classes={classes} -> class ids {ids}")
    return ids


assert run("index + 1", [1, 2, 3], 80) == [0, 1, 2]
assert run("background only", [], 80) == []
assert run("0/255 binary mask", [255], 80) == []
assert run("1 mixed with 255", [1, 255], 80) == [0]
print("all checks passed")
