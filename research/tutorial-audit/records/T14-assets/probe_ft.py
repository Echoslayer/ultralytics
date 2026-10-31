import tempfile, os, yaml, re, io, logging
from pathlib import Path
os.chdir(tempfile.mkdtemp())
from ultralytics import YOLO
from ultralytics.utils import LOGGER
from ultralytics.nn.tasks import DetectionModel
# transfer count: coco -> 5 classes, documented "696 of 708"
s = logging.StreamHandler(buf := io.StringIO()); LOGGER.addHandler(s)
ck = YOLO("yolo26n.pt").model
m = DetectionModel("yolo26n.yaml", nc=5, verbose=False)
m.load(ck, verbose=True)
print("LOG5:", [l for l in buf.getvalue().splitlines() if "ransferred" in l or "Remapped" in l])
print("target state tensors", len(m.state_dict()), "src", len(ck.state_dict()))
# freeze claims
names = [type(x).__name__ for x in ck.model]
print("layers 0-11:", list(enumerate(names[:12])))
print("Detect idx:", len(names)-1, names[-1])
print("head attrs:", [a for a in ("cv2","cv3","one2one_cv2","one2one_cv3") if hasattr(ck.model[-1],a)])
# optimizer=auto threshold and lr0 ignored
from ultralytics.engine.trainer import BaseTrainer
import inspect
src = inspect.getsource(BaseTrainer.build_optimizer)
print([l.strip() for l in src.splitlines() if "10000" in l or "10_000" in l or "MuSGD" in l or "lr0" in l or "auto" in l][:14])
