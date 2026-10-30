"""T13: run docs/en/guides/coco-json-training.md on COCO8 converted to COCO JSON, then test its cache-key warning."""

import json
import os
import shutil
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "t13out"
shutil.rmtree(OUT, ignore_errors=True)
OUT.mkdir()
os.environ["YOLO_CONFIG_DIR"] = str(OUT / "cfg")
os.chdir(OUT)

from PIL import Image  # noqa: E402

from ultralytics.data.utils import check_det_dataset  # noqa: E402

# Guide's classes, verbatim (Full Implementation minus the last two lines that start a 100-epoch run)
src = (HERE / "coco_full.py").read_text().splitlines()
exec("\n".join(src[:-2]))

# --- Build my_dataset/ in the guide's layout from COCO8, with non-contiguous category ids ---
c8 = check_det_dataset("coco8.yaml")
root = OUT / "my_dataset"
names = c8["names"]
used = set()
for split in ("train", "val"):
    (root / "images" / split).mkdir(parents=True)
    imgs, anns = [], []
    for i, im in enumerate(sorted((Path(c8["path"]) / "images" / split).glob("*.jpg"))):
        shutil.copy(im, root / "images" / split / im.name)
        w, h = Image.open(im).size
        imgs.append({"id": i, "file_name": im.name, "width": w, "height": h})
        lb = Path(c8["path"]) / "labels" / split / f"{im.stem}.txt"
        for line in lb.read_text().splitlines() if lb.exists() else []:
            c, cx, cy, bw, bh = map(float, line.split())
            used.add(int(c))
            anns.append(
                {
                    "id": len(anns),
                    "image_id": i,
                    "category_id": int(c) * 10 + 7,  # non-contiguous ids
                    "bbox": [round((cx - bw / 2) * w, 2), round((cy - bh / 2) * h, 2), round(bw * w, 2), round(bh * h, 2)],
                    "iscrowd": 0,
                }
            )
    (root / "annotations").mkdir(exist_ok=True)
    cats = [{"id": k * 10 + 7, "name": names[k]} for k in sorted(names)]
    (root / "annotations" / f"instances_{split}.json").write_text(
        json.dumps({"images": imgs, "annotations": anns, "categories": cats})
    )
yaml = f"""path: {(root / "images").as_posix()}
train: train
val: val
train_json: {(root / "annotations" / "instances_train.json").as_posix()}
val_json: {(root / "annotations" / "instances_val.json").as_posix()}
names:
""" + "".join(f"    {k}: {v}\n" for k, v in names.items())
(root / "dataset.yaml").write_text(yaml)

# --- A: training through COCOTrainer ---
print("== A: train 1 epoch ==")
from ultralytics import YOLO  # noqa: E402

model = YOLO(str(HERE / "yolo26n.pt"))
model.train(
    data=str(root / "dataset.yaml"), epochs=1, imgsz=320, device="cpu", workers=0, trainer=COCOTrainer, plots=False
)
m = model.trainer.metrics
print("mAP50-95:", round(m["metrics/mAP50-95(B)"], 4), "mAP50:", round(m["metrics/mAP50(B)"], 4))
print("cache files:", sorted(p.name for p in (root / "annotations").glob("*.cache")))


# --- B: does a same-size JSON edit reuse the stale cache, as the warning says? ---
print("== B: cache key ==")
parses = []
orig_cache_labels = COCODataset.cache_labels


def spy(self, path=Path("./labels.cache")):
    parses.append(path.name)
    return orig_cache_labels(self, path)


COCODataset.cache_labels = spy


def build():
    parses.clear()
    ds = COCODataset(img_path=str(root / "images" / "train"), json_file=str(jf), imgsz=320, augment=False)
    return ds, bool(parses)


jf = root / "annotations" / "instances_train.json"
ds, parsed = build()
print("rerun, no edit: parsed JSON =", parsed, "| first box:", ds.labels[0]["bboxes"][0].round(4).tolist())

coco = json.loads(jf.read_text())
before = coco["annotations"][0]["bbox"][2]
size0 = jf.stat().st_size
text = jf.read_text()
old = json.dumps(coco["annotations"][0]["bbox"])
b = coco["annotations"][0]["bbox"]
new_bbox = [b[0], b[1], b[2], b[3]]
# Same-length edit: change the first digit of the width (e.g. 1xx.yy -> 2xx.yy)
s = str(b[2])
s2 = ("2" if s[0] != "2" else "3") + s[1:]
new_bbox[2] = float(s2)
new = json.dumps(new_bbox)
assert len(new) == len(old) and text.count(old) == 1
jf.write_text(text.replace(old, new))
print(f"edited width {before} -> {s2}; JSON size {size0} -> {jf.stat().st_size}")
ds, parsed = build()
print("rerun after same-size edit: parsed JSON =", parsed, "| first box:", ds.labels[0]["bboxes"][0].round(4).tolist())

# --- C: standalone model.val() (the guide's note says all metrics are 0) ---
print("== C: standalone val ==")
best = model.trainer.best
mv = YOLO(str(best)).val(data=str(root / "dataset.yaml"), imgsz=320, device="cpu", workers=0, plots=False, verbose=False)
print("standalone mAP50-95:", mv.box.map)
