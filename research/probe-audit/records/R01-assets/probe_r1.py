"""Round-1 probes on recently merged inference changes (#26942, #26939). Prints findings, never asserts."""

import math
import sys
import time
from pathlib import Path

sys.path.insert(0, sys.argv[1])  # upstream worktree
OUT = Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)

import cv2
import numpy as np
import torch

import ultralytics
from ultralytics import YOLO
from ultralytics.data.loaders import LoadImagesAndVideos
from ultralytics.utils import ASSETS

print("ultralytics", ultralytics.__version__, ultralytics.__file__, "torch", torch.__version__)
BUS = ASSETS / "bus.jpg"


def matmul_ms():
    a = torch.randn(1024, 1024)
    t = time.perf_counter()
    for _ in range(20):
        a @ a
    return (time.perf_counter() - t) * 50


# P1 #26942: does ONNX/OpenVINO CPU predict leave torch's global thread count capped?
print("\n== P1 thread cap")
t0, ms0 = torch.get_num_threads(), matmul_ms()
onnx = YOLO("yolo26n.pt").export(format="onnx", imgsz=64, project=str(OUT))
YOLO(onnx)(BUS, imgsz=64, verbose=False)
t1, ms1 = torch.get_num_threads(), matmul_ms()
print(f"threads before={t0} after_onnx_predict={t1}; 1024x1024 matmul ms before={ms0:.1f} after={ms1:.1f}")
torch.set_num_threads(t0)

# P2 #26939: which frames does vid_stride read, and does len() match what is yielded?
print("\n== P2 vid_stride frames")
video = OUT / "index.avi"
N = 10
w = cv2.VideoWriter(str(video), cv2.VideoWriter_fourcc(*"MJPG"), 10, (64, 64))
for i in range(N):
    w.write(np.full((64, 64, 3), i * 20 + 10, np.uint8))  # frame index encoded in brightness
w.release()
for stride in (1, 2, 3, 4, 10, 11):
    ds = LoadImagesAndVideos(str(video), vid_stride=stride)
    got, labels = [], []
    for _, ims, info in ds:
        got += [round((float(im.mean()) - 10) / 20) for im in ims]
        labels += info
    expect = list(range(0, N, stride))
    ok = got == expect and ds.frames == math.ceil(N / stride) == len(got)  # len(ds) counts batches, not frames
    print(f"stride={stride} frames={ds.frames} read={got} expect={expect} {'OK' if ok else 'MISMATCH'} last_label={labels[-1][-40:]!r}")

# P3 #26939: export imgsz becomes the default for every export, incl. static non-square
print("\n== P3 export imgsz default")
for kw in ({"imgsz": [96, 128]}, {"imgsz": [96, 128], "dynamic": True}, {"imgsz": 96}):
    f = YOLO("yolo26n.pt").export(format="onnx", project=str(OUT / str(len(str(kw)))), **kw)
    m = YOLO(f)
    try:
        r = m(BUS, verbose=False)[0]
        res = f"pred ok, input {tuple(r.speed and m.predictor.imgsz)}, boxes={len(r.boxes)}"
    except Exception as e:
        res = f"pred FAIL {type(e).__name__}: {e}"
    print(kw, "-> overrides imgsz", m.overrides.get("imgsz"), "|", res)
