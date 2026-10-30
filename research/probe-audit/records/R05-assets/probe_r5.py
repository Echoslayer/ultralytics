"""Round-5 probes on issue #26795: YOLO26-seg masks miss parts of objects that fill 80-90% of the image. Prints only."""

import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1])
OUT = Path(sys.argv[2]).resolve()
OUT.mkdir(parents=True, exist_ok=True)

import cv2
import torch

import ultralytics
from ultralytics import YOLO
from ultralytics.utils import ASSETS, ops

print("ultralytics", ultralytics.__version__, ultralytics.__file__, "torch", torch.__version__)
seen = []
_crop = ops.crop_mask


def spy(masks, boxes):  # record the uncropped binary masks and boxes before crop_mask zeroes the outside
    seen.append((masks.clone(), boxes.clone()))
    return _crop(masks, boxes)


ops.crop_mask = spy
model = YOLO("yolo26n-seg.pt")
im = cv2.imread(str(ASSETS / "bus.jpg"))
bus = model(im, verbose=False)[0]
i = int((bus.boxes.cls == 5).nonzero()[0])  # COCO class 5 = bus
x1, y1, x2, y2 = bus.boxes.xyxy[i].round().int().tolist()
print("bus box in bus.jpg", (x1, y1, x2, y2), "image", im.shape[:2])

for fill in (0.5, 0.8, 0.9, 0.98):  # bus box side / crop side
    mx, my = int((x2 - x1) * (1 / fill - 1) / 2), int((y2 - y1) * (1 / fill - 1) / 2)
    crop = im[max(y1 - my, 0) : y2 + my, max(x1 - mx, 0) : x2 + mx]
    for imgsz in (640, 320):
        for retina in (False, True):
            seen.clear()
            r = model(crop, imgsz=imgsz, retina_masks=retina, verbose=False)[0]
            if r.boxes is None or not (r.boxes.cls == 5).any():
                print(f"fill={fill} imgsz={imgsz} retina={retina}: no bus detected")
                continue
            j = int((r.boxes.conf * (r.boxes.cls == 5)).argmax())
            raw, boxes = seen[-1]
            m, b = raw[j].bool(), boxes[j].round().int().tolist()
            inside = torch.zeros_like(m)
            inside[b[1] : b[3], b[0] : b[2]] = True
            lost = (m & ~inside).sum().item() / max(m.sum().item(), 1)
            kept = r.masks.data[j].float().mean().item()
            print(f"fill={fill} imgsz={imgsz} retina={retina!s:5} crop={crop.shape[:2]} conf={r.boxes.conf[j]:.2f} "
                  f"box={b} mask_area={kept:.3f} of frame, uncropped mask outside box={lost:.3%}")
            if fill == 0.9 and imgsz == 640 and not retina:
                cv2.imwrite(str(OUT / "fill90.jpg"), r.plot(boxes=True))
ops.crop_mask = _crop
