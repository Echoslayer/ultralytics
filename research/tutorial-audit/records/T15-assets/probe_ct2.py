"""Check what custom-trainer.md claims about behavior, not only that the examples exit 0."""
import re, sys, textwrap
from pathlib import Path

import torch

from ultralytics import YOLO, settings
from ultralytics.utils import RUNS_DIR

print("RUNS_DIR", RUNS_DIR)
assert RUNS_DIR.parts[0] == "runs"  # YOLO_CONFIG_DIR isolates the run from the global settings
text = Path(sys.argv[1]).read_text()
blocks = [textwrap.dedent(m.group(2)) for m in re.finditer(r"^([ \t]*)```python[^\n]*\n(.*?)^\1```", text, re.S | re.M)]
get = lambda k: next(b for b in blocks if k in b)
defs = lambda code: code.split('\nmodel = ')[0]
kw = dict(data="coco8.yaml", imgsz=160, device="cpu", workers=0, plots=False, verbose=False, batch=4, nbs=4)

# freezing
ns = {}; exec(defs(get("class FreezingTrainer")), ns)
m = YOLO("yolo26n.pt"); log = []
def snap(t):
    p = dict(t.model.named_parameters())
    log.append((t.epoch, sum(v.requires_grad for k, v in p.items() if k.startswith("model.0.")), p["model.0.conv.weight"].detach().clone(), p["model.5.conv.weight" if "model.5.conv.weight" in p else "model.0.conv.weight"].requires_grad))
m.add_callback("on_train_epoch_end", snap)
m.train(epochs=8, freeze=10, trainer=ns["FreezingTrainer"], **kw)
for a, b in zip(log, log[1:]):
    print(f"epoch {b[0]} layer0 trainable={b[1]} weight changed={not torch.equal(a[2], b[2])}")

# best by mAP50
ns = {}; exec(defs(get("class CustomSaveTrainer")), ns)
m = YOLO("yolo26n.pt"); rows = []
m.add_callback("on_fit_epoch_end", lambda t: rows.append((t.epoch, round(t.fitness, 4), round(t.best_fitness, 4), round(t.metrics["metrics/mAP50(B)"], 4), round(t.metrics["metrics/mAP50-95(B)"], 4))))
m.train(epochs=3, trainer=ns["CustomSaveTrainer"], **kw)
print("epoch, fitness, best, map50, map:", rows)
