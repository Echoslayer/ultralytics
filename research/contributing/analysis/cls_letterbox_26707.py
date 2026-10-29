"""#26707: do docs' letterbox custom transforms reach train, val, and predict-from-best.pt without cropping?"""

import json
import os
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
import torch
import torchvision.transforms as T
from PIL import Image

WORK = Path(sys.argv[1]).resolve()
IMGSZ = 64


def make(path, h, w):
    """Gray image with distinct colored 6px squares in each corner (BGR)."""
    im = np.full((h, w, 3), 128, np.uint8)
    for (y, x), c in zip(
        ((0, 0), (0, w - 6), (h - 6, 0), (h - 6, w - 6)), ((0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255))
    ):
        im[y : y + 6, x : x + 6] = c
    path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(path), im)


data = WORK / "data"
for split in ("train", "val"):
    for cls in ("a", "b"):
        for i, (h, w) in enumerate(((64, 256), (256, 64), (128, 128), (64, 256))):
            make(data / split / cls / f"{i}.png", h, w)
wide = data / "val" / "a" / "0.png"


def corners(t):
    """Count corner markers visible in a CHW float tensor in [0,1]."""
    im = (t.permute(1, 2, 0).numpy() * 255).astype(np.uint8)  # RGB
    want = {"red": (255, 0, 0), "green": (0, 255, 0), "blue": (0, 0, 255), "yellow": (255, 255, 0)}
    return sorted(k for k, c in want.items() if (np.abs(im.astype(int) - c).sum(-1) < 60).any())


from ultralytics import YOLO
from ultralytics.data.augment import ClassifyLetterBox, classify_transforms
from ultralytics.data.dataset import ClassificationDataset
from ultralytics.models.yolo.classify import ClassificationTrainer, ClassificationValidator


# --- verbatim from docs/en/tasks/classify.md "Custom transforms" -----------------------------------------------------
class CustomizedDataset(ClassificationDataset):
    def __init__(self, root: str, args, augment: bool = False, prefix: str = "", names=None):
        super().__init__(root, args, augment, prefix, names)
        letterbox = T.Compose([np.asarray, ClassifyLetterBox(args.imgsz), T.ToPILImage()])
        train_transforms = T.Compose(
            [
                letterbox,
                T.RandomHorizontalFlip(p=args.fliplr),
                T.RandomVerticalFlip(p=args.flipud),
                T.RandAugment(interpolation=T.InterpolationMode.BILINEAR),
                T.ColorJitter(brightness=args.hsv_v, contrast=args.hsv_v, saturation=args.hsv_s, hue=args.hsv_h),
                T.ToTensor(),
                T.Normalize(mean=torch.tensor(0), std=torch.tensor(1)),
                T.RandomErasing(p=args.erasing, inplace=True),
            ]
        )
        val_transforms = T.Compose([letterbox, T.ToTensor(), T.Normalize(mean=torch.tensor(0), std=torch.tensor(1))])
        self.torch_transforms = train_transforms if augment else val_transforms


class CustomizedTrainer(ClassificationTrainer):
    def build_dataset(self, img_path: str, mode: str = "train", batch=None):
        return CustomizedDataset(
            root=img_path,
            args=self.args,
            augment=mode == "train",
            prefix="train" if mode == "train" else self.args.split,
            names=self.data["names"],
        )


class CustomizedValidator(ClassificationValidator):
    def build_dataset(self, img_path: str):
        return CustomizedDataset(root=img_path, args=self.args, augment=False, prefix=self.args.split, names=self.names)


# ---------------------------------------------------------------------------------------------------------------------

report = {}
model = YOLO("yolo26n-cls.yaml")
model.train(
    data=str(data),
    trainer=CustomizedTrainer,
    epochs=1,
    imgsz=IMGSZ,
    batch=4,
    workers=0,
    project=str(WORK / "runs"),
    name="t",
    exist_ok=True,
    plots=False,
    val=True,
)
trainer = model.trainer
ds = trainer.train_loader.dataset
report["train_transform_steps"] = [type(t).__name__ for t in ds.torch_transforms.transforms]
ds_noaug = CustomizedDataset(str(data / "train"), trainer.args, augment=False, names=trainer.data["names"])
report["val_transform_on_wide"] = corners(ds_noaug.torch_transforms(Image.open(wide).convert("RGB")))
best = Path(trainer.best)
report["best_pt"] = str(best)

# Predict from best.pt in a fresh model object; capture exactly what reaches the network.
seen = {}
m2 = YOLO(best)


def grab(predictor):
    orig = predictor.preprocess

    def wrapped(img):
        out = orig(img)
        seen["shape"] = tuple(out.shape)
        seen["corners"] = corners(out[0].float().cpu().clamp(0, 1))
        return out

    predictor.preprocess = wrapped


m2.add_callback("on_predict_start", grab)
m2.predict(str(wide), imgsz=IMGSZ, verbose=False)
report["checkpoint_transforms"] = repr(getattr(m2.model, "transforms", None))[:400]
report["predictor_transforms"] = repr(m2.predictor.transforms)[:400]
report["predict_input"] = seen

# Same checkpoint under opt-in restricted loading, in a separate process so the env flag applies at import.
probe = "from ultralytics import YOLO; import sys; YOLO(sys.argv[1]).predict(sys.argv[2], imgsz=64, verbose=False)"
env = {**os.environ, "ULTRALYTICS_SAFE_LOAD": "1"}
r = subprocess.run(
    [sys.executable, "-I", "-c", probe, str(best), str(wide)], check=False, env=env, capture_output=True, text=True
)
report["safe_load_predict"] = "ok" if r.returncode == 0 else r.stderr.strip().splitlines()[-1][:400]

report["default_classify_transforms_on_wide"] = corners(classify_transforms(IMGSZ)(Image.open(wide).convert("RGB")))
print("REPORT " + json.dumps(report, indent=2))
(WORK / "report.json").write_text(json.dumps(report, indent=2))
