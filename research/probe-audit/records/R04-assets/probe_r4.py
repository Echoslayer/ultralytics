"""Round-4 probes: combinations the docs barely cover (quantize/half on CPU ONNX, rect val, OBB/pose tracking, batch on static ONNX). Prints only."""

import sys
import warnings
from pathlib import Path

sys.path.insert(0, sys.argv[1])
OUT = Path(sys.argv[2]).resolve()
OUT.mkdir(parents=True, exist_ok=True)

import cv2
import numpy as np
import onnx
import torch

import ultralytics
from ultralytics import YOLO
from ultralytics.utils import ASSETS

print("ultralytics", ultralytics.__version__, ultralytics.__file__, "torch", torch.__version__)
BUS, BOATS = ASSETS / "bus.jpg", Path("boats.jpg").resolve()


def probe(name, fn):
    try:
        print(f"{name}: OK {fn()}")
    except Exception as e:
        print(f"{name}: FAIL {type(e).__name__}: {str(e)[:300]}")


def onnx_dtypes(f):
    m = onnx.load(f)
    init = {onnx.TensorProto.DataType.Name(t.data_type) for t in m.graph.initializer}
    io = [onnx.TensorProto.DataType.Name(i.type.tensor_type.elem_type) for i in [*m.graph.input, *m.graph.output]]
    return f"initializers={sorted(init)} io={io}"


def export(w, sub, **kw):
    """Export, then move the file aside: ONNX export always writes next to the weights, so exports overwrite each other."""
    f = Path(YOLO(w).export(format="onnx", imgsz=320, **kw))
    dst = OUT / f"{f.stem}_{sub}.onnx"
    f.replace(dst)
    return str(dst)


# P1/P2: FP16 ONNX on CPU, via quantize=16 and deprecated half=True; compare with FP32
print("\n== P1/P2 FP16 ONNX on CPU")
f32 = export("yolo26n.pt", "fp32")
f16 = export("yolo26n.pt", "q16", quantize=16)
fh = export("yolo26n.pt", "half", half=True)
for tag, f in (("fp32", f32), ("quantize=16", f16), ("half=True", fh)):
    print(tag, Path(f).name, f"{Path(f).stat().st_size / 1e6:.1f}MB", onnx_dtypes(f))
b32 = YOLO(f32)(BUS, imgsz=320, verbose=False)[0].boxes
for tag, f in (("quantize=16", f16), ("half=True", fh)):
    def cmp(f=f):
        b = YOLO(f)(BUS, imgsz=320, verbose=False)[0].boxes
        d = (b.xyxy - b32.xyxy).abs().max().item() if len(b) == len(b32) else "n/a"
        return f"boxes {len(b)} vs fp32 {len(b32)}, max xyxy diff={d}, cls equal={b.cls.tolist() == b32.cls.tolist()}"
    probe(f"predict {tag}", cmp)
probe("val quantize=16 onnx", lambda: round(YOLO(f16).val(data="coco8.yaml", imgsz=320, batch=1, plots=False,
                                                         verbose=False, project=str(OUT), name="v16").box.map, 4))
probe("val fp32 onnx", lambda: round(YOLO(f32).val(data="coco8.yaml", imgsz=320, batch=1, plots=False,
                                                  verbose=False, project=str(OUT), name="v32").box.map, 4))
probe("predict pt half=True on cpu", lambda: str(YOLO("yolo26n.pt")(BUS, imgsz=320, half=True, verbose=False)[0].boxes.data.dtype))

# P3: val with rect=True on static vs dynamic ONNX
print("\n== P3 rect val on ONNX")
fd = export("yolo26n.pt", "dyn", dynamic=True)
for tag, f in (("pt", "yolo26n.pt"), ("static", f32), ("dynamic", fd)):
    def v(f=f):
        val = YOLO(f).val(data="coco8.yaml", imgsz=320, batch=4, rect=True, plots=False, verbose=False,
                          project=str(OUT), name=f"rect_{tag}")
        return f"map={val.box.map:.4f}"
    probe(f"val rect=True {tag}", v)

# P4: tracking with OBB and pose on a synthetic panning video, pt and ONNX
print("\n== P4 OBB/pose tracking")


def pan_video(img, name, n=8, step=6):
    im = cv2.imread(str(img))
    h, w = im.shape[:2]
    ch, cw = int(h * 0.8), int(w * 0.8)
    f = OUT / name
    vw = cv2.VideoWriter(str(f), cv2.VideoWriter_fourcc(*"MJPG"), 10, (cw, ch))
    for i in range(n):
        vw.write(np.ascontiguousarray(im[:ch, i * step : i * step + cw]))
    vw.release()
    return f


videos = {"obb": pan_video(BOATS, "boats.avi"), "pose": pan_video(BUS, "bus.avi")}
for task, w in (("obb", "yolo26n-obb.pt"), ("pose", "yolo26n-pose.pt")):
    for tag, m in (("pt", w), ("onnx", export(w, f"{task}_onnx"))):
        def t(task=task, m=m):
            ids, n = [], []
            for r in YOLO(m).track(str(videos[task]), imgsz=320, stream=True, verbose=False, persist=True):
                obj = r.obb if task == "obb" else r.boxes
                n.append(len(obj))
                ids.append(set(obj.id.int().tolist()) if obj.id is not None else set())
                if task == "pose":
                    assert r.keypoints is None or len(r.keypoints) == len(r.boxes), "keypoints/boxes length mismatch"
            stable = len(ids[1] & ids[-1]) if len(ids) > 1 else 0
            return f"frames={len(n)} dets={n} ids_frame1={len(ids[1])} kept_to_last={stable}"
        probe(f"track {task} {tag}", t)

# P5: static batch=1 ONNX given a list of images
print("\n== P5 batch on static ONNX")
probe("list of 3, static batch=1", lambda: [len(r.boxes) for r in YOLO(f32)([BUS, BUS, BOATS], imgsz=320, verbose=False)])
probe("list of 3, batch=3 arg", lambda: [len(r.boxes) for r in YOLO(f32)([BUS, BUS, BOATS], imgsz=320, batch=3, verbose=False)])
fb = export("yolo26n.pt", "b2", batch=2)
probe("list of 3, static batch=2 export", lambda: [len(r.boxes) for r in YOLO(fb)([BUS, BUS, BOATS], imgsz=320, verbose=False)])
