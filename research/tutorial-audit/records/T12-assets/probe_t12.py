"""T12: run docs/en/guides/isolating-segmentation-objects.md Full Example, then compare its contour mask to the model mask."""

import os
from pathlib import Path

import cv2
import numpy as np

from ultralytics import YOLO
from ultralytics.utils import ASSETS
from ultralytics.utils.ops import scale_masks

HERE = Path(__file__).parent
OUT = HERE / "t12out"
OUT.mkdir(exist_ok=True)
os.chdir(OUT)  # the docs script writes PNGs into cwd

model = YOLO(str(HERE / "yolo26n-seg.pt"))
sources = [str(ASSETS / "bus.jpg"), str(ASSETS / "zidane.jpg"), str(HERE / "boats.jpg")]

# --- A: Full Example, verbatim except source ---
print("== A: Full Example ==")
for src in sources:
    results = model.predict(source=src, verbose=False)
    for r in results:
        img = np.copy(r.orig_img)
        img_name = Path(r.path).stem
        for ci, c in enumerate(r):
            label = c.names[c.boxes.cls.tolist().pop()]
            b_mask = np.zeros(img.shape[:2], np.uint8)
            contour = c.masks.xy[0].astype(np.int32).reshape(-1, 1, 2)
            cv2.drawContours(b_mask, [contour], -1, (255, 255, 255), cv2.FILLED)
            mask3ch = cv2.cvtColor(b_mask, cv2.COLOR_GRAY2BGR)
            isolated = cv2.bitwise_and(mask3ch, img)
            cv2.imwrite(f"{img_name}_{label}-{ci}.png", isolated)
    print(src, "detections:", len(results[0]))
print("files written:", len(list(OUT.glob("*.png"))))

# --- B: contour mask vs model mask at original resolution ---
print("== B: contour mask vs model mask ==")
for src in sources:
    r = model.predict(source=src, verbose=False)[0]
    h, w = r.orig_shape
    native = scale_masks(r.masks.data[None].float(), (h, w))[0] > 0.5  # model mask at orig size
    for ci, c in enumerate(r):
        b_mask = np.zeros((h, w), np.uint8)
        pts = c.masks.xy[0]
        contour = pts.astype(np.int32).reshape(-1, 1, 2)
        cv2.drawContours(b_mask, [contour], -1, (255, 255, 255), cv2.FILLED)
        m = native[ci].cpu().numpy()
        n_parts = len(cv2.findContours(c.masks.data[0].byte().cpu().numpy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0])
        b = b_mask > 0
        iou = (b & m).sum() / max((b | m).sum(), 1)
        print(
            f"{Path(src).stem} #{ci} {c.names[int(c.boxes.cls)]:<10} parts={n_parts} pts={len(pts):4d} "
            f"model_px={m.sum():7d} contour_px={b.sum():7d} IoU={iou:.3f}"
        )

# --- C: empty contour (a mask with no pixels) ---
print("== C: empty contour ==")
empty = np.zeros((0, 2), np.float32).astype(np.int32).reshape(-1, 1, 2)
try:
    cv2.drawContours(np.zeros((10, 10), np.uint8), [empty], -1, 255, cv2.FILLED)
    print("drawContours with (0,1,2): no error")
except cv2.error as e:
    print("drawContours with (0,1,2): cv2.error", str(e).splitlines()[-1][:120])

# --- D: crop tip and FAQ crop snippet ---
print("== D: crop snippets ==")
r = model.predict(source=sources[0], verbose=False)[0]
c = r[0]
x1, y1, x2, y2 = c.boxes.xyxy.cpu().numpy().squeeze().astype(np.int32)
print("tip crop box:", (x1, y1, x2, y2))
x1, y1, x2, y2 = r.boxes.xyxy[0].cpu().numpy().astype(np.int32)
print("faq crop box:", (x1, y1, x2, y2))

# --- E: transparent PNG round-trip ---
print("== E: transparent PNG ==")
img = np.copy(r.orig_img)
b_mask = np.zeros(img.shape[:2], np.uint8)
cv2.drawContours(b_mask, [c.masks.xy[0].astype(np.int32).reshape(-1, 1, 2)], -1, (255, 255, 255), cv2.FILLED)
cv2.imwrite("alpha.png", np.dstack([img, b_mask]))
back = cv2.imread("alpha.png", cv2.IMREAD_UNCHANGED)
print("read back shape:", back.shape, "alpha values:", np.unique(back[..., 3]).tolist())

# --- F: no source tip ---
print("== F: predict() without source ==")
res = model.predict(verbose=False)
print("n results:", len(res), [Path(x.path).name for x in res])
