"""Round-3 probes: the Results type/shape tables in docs/en/tasks/*.md, checked on .pt and ONNX. Prints only."""

import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1])
OUT = Path(sys.argv[2]).resolve()

import torch

import ultralytics
from ultralytics import YOLO
from ultralytics.utils import ASSETS

print("ultralytics", ultralytics.__version__, ultralytics.__file__, "torch", torch.__version__)
FIELDS = {  # task: (weights, image, documented attributes)
    "detect": ("yolo26n.pt", "bus.jpg", ["boxes.data", "boxes.xyxy", "boxes.conf", "boxes.cls"]),
    "segment": ("yolo26n-seg.pt", "bus.jpg", ["masks.data", "masks.xy", "masks.xyn", "boxes.cls"]),
    "pose": ("yolo26n-pose.pt", "bus.jpg", ["keypoints.data", "keypoints.xy", "keypoints.xyn", "boxes.xyxy"]),
    "obb": ("yolo26n-obb.pt", "boats.jpg", ["obb.data", "obb.xywhr", "obb.xyxyxyxy", "obb.conf", "obb.cls"]),
    "classify": ("yolo26n-cls.pt", "bus.jpg", ["probs.data", "probs.top1", "probs.top1conf", "probs.top5"]),
}


def describe(v):
    if isinstance(v, torch.Tensor):
        return f"{v.dtype} {tuple(v.shape)}"
    if isinstance(v, list):
        inner = describe(v[0]) if v else "empty"
        return f"list[{len(v)}] of {inner}"
    if hasattr(v, "dtype"):  # numpy
        return f"np.{v.dtype} {v.shape}"
    return type(v).__name__


def get(r, path):
    for p in path.split("."):
        r = getattr(r, p)
    return r


for task, (w, img, attrs) in FIELDS.items():
    src = ASSETS / img
    if not src.exists():
        src = f"https://ultralytics.com/images/{img}"
    pt = YOLO(w)
    onnx = YOLO(pt.export(format="onnx", imgsz=320 if task != "classify" else 224))
    for name, m in (("pt", pt), ("onnx", onnx)):
        try:
            r = m(src, imgsz=320 if task != "classify" else 224, verbose=False)[0]
        except Exception as e:
            print(f"{task} {name}: PREDICT FAIL {type(e).__name__}: {str(e)[:200]}")
            continue
        for a in attrs:
            try:
                print(f"{task:8} {name:4} {a:18} {describe(get(r, a))}")
            except Exception as e:
                print(f"{task:8} {name:4} {a:18} FAIL {type(e).__name__}: {str(e)[:200]}")

# P2 obb.md: xyxyxyxy2xywhr(result.obb.xyxyxyxy) gives w >= h and rotation in [-pi/4, 3pi/4), same rectangle
import math

from ultralytics.utils.ops import xywhr2xyxyxyxy, xyxyxyxy2xywhr

print("\n== P2 obb long-edge snippet")
for name, w in (("pt", "yolo26n-obb.pt"), ("onnx", "yolo26n-obb.onnx")):
    o = YOLO(w)(ASSETS / "boats.jpg" if (ASSETS / "boats.jpg").exists() else "boats.jpg", imgsz=320, verbose=False)[0].obb
    c = xyxyxyxy2xywhr(o.xyxyxyxy)
    c = torch.as_tensor(c)
    raw_short = int((o.xywhr[:, 2] < o.xywhr[:, 3]).sum())
    bad_wh = int((c[:, 2] < c[:, 3] - 1e-3).sum())
    bad_ang = int(((c[:, 4] < -math.pi / 4 - 1e-4) | (c[:, 4] >= 3 * math.pi / 4 + 1e-4)).sum())
    back = torch.as_tensor(xywhr2xyxyxyxy(c))
    # same rectangle: compare sorted corner sets
    diff = (back.sort(dim=1)[0] - o.xyxyxyxy.sort(dim=1)[0]).abs().max().item()
    print(f"{name}: n={len(c)} raw w<h={raw_short} after w<h={bad_wh} angle_out={bad_ang} "
          f"angle_range=[{c[:, 4].min():.3f},{c[:, 4].max():.3f}] corner_maxdiff={diff:.3f}")

# P3 pose.md keypoint index map vs. names carried by the model / dataset yaml
print("\n== P3 pose keypoint names")
from ultralytics.utils import YAML

doc = ["nose", "left_eye", "right_eye", "left_ear", "right_ear", "left_shoulder", "right_shoulder", "left_elbow",
       "right_elbow", "left_wrist", "right_wrist", "left_hip", "right_hip", "left_knee", "right_knee", "left_ankle",
       "right_ankle"]
yaml_names = YAML.load(Path(sys.argv[1]) / "ultralytics/cfg/datasets/coco-pose.yaml").get("kpt_names")
print("yaml kpt_names:", yaml_names)
for name, w in (("pt", "yolo26n-pose.pt"), ("onnx", "yolo26n-pose.onnx")):
    m = YOLO(w)
    m(ASSETS / "bus.jpg", imgsz=320, verbose=False)
    meta = getattr(m.predictor.model, "kpt_names", None) or getattr(m.model, "kpt_names", None)
    print(f"{name}: model kpt_names={meta} kpt_shape={getattr(m.predictor.model, 'kpt_shape', None)}")
