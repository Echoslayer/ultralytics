"""Round-2 probes on #26937: use a mid-run distillation checkpoint in ways the PR table does not list."""

import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1])
OUT = Path(sys.argv[2]).resolve()

import torch

import ultralytics
from ultralytics import YOLO
from ultralytics.utils import ASSETS

print("ultralytics", ultralytics.__version__, ultralytics.__file__, "torch", torch.__version__)
ckpt = next(OUT.rglob("epoch1.pt"), None)
if ckpt is None:
    YOLO("yolo26n.pt").train(
        data="coco8.yaml", distill_model="yolo26s.pt", epochs=2, save_period=1, imgsz=160, batch=4, workers=0,
        project=str(OUT), name="distill", exist_ok=True, plots=False, verbose=False,
    )
    ckpt = next(OUT.rglob("epoch1.pt"))
raw = torch.load(ckpt, map_location="cpu", weights_only=False)
print("checkpoint", ckpt.name, "model type", type(raw.get("ema") or raw["model"]).__name__)


def probe(name, fn):
    try:
        print(f"{name}: OK {fn()}")
    except Exception as e:
        print(f"{name}: FAIL {type(e).__name__}: {str(e)[:300]}")


probe("YOLO(ckpt) type", lambda: type(YOLO(ckpt).model).__name__)
probe("predict", lambda: len(YOLO(ckpt)(ASSETS / "bus.jpg", imgsz=160, verbose=False)[0].boxes))
probe("val", lambda: round(YOLO(ckpt).val(data="coco8.yaml", imgsz=160, batch=4, workers=0, plots=False,
                                            verbose=False, project=str(OUT), name="val").box.map, 4))
probe("fuse+predict", lambda: len(YOLO(ckpt).fuse()(ASSETS / "bus.jpg", imgsz=160, verbose=False)[0].boxes))


def autobackend():
    from ultralytics.nn.autobackend import AutoBackend

    m = AutoBackend(str(ckpt), device=torch.device("cpu"))
    return f"{type(m.model).__name__ if hasattr(m, 'model') else type(m).__name__}, names={len(m.names)}"


probe("AutoBackend", autobackend)


def save_reload():
    m = YOLO(ckpt)
    m.save(OUT / "saved.pt")
    return type(YOLO(OUT / "saved.pt").model).__name__


probe("save+reload", save_reload)


def safe_load():  # fresh process: ULTRALYTICS_SAFE_LOAD is read at import
    code = f"import sys; sys.path.insert(0, {sys.argv[1]!r}); from ultralytics import YOLO; print(type(YOLO({str(ckpt)!r}).model).__name__)"
    r = subprocess.run([sys.executable, "-I", "-c", code], capture_output=True, text=True,
                       env={**os.environ, "ULTRALYTICS_SAFE_LOAD": "1"})
    if r.returncode:
        raise RuntimeError(r.stderr.strip().splitlines()[-1])
    return r.stdout.strip().splitlines()[-1]


probe("safe load", safe_load)
probe("torchscript export", lambda: Path(YOLO(ckpt).export(format="torchscript", imgsz=160)).name)
