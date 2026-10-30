"""T13c: which image-folder changes invalidate the COCO JSON cache (the hash stats the folder, not the files)?"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "t13out"
os.environ["YOLO_CONFIG_DIR"] = str(OUT / "cfg")
src = (HERE / "coco_full.py").read_text().splitlines()
exec("\n".join(src[:-2]))

root = OUT / "my_dataset"
jf = root / "annotations" / "instances_train.json"
imgs = root / "images" / "train"
parses = []
orig = COCODataset.cache_labels
COCODataset.cache_labels = lambda self, path=Path("./labels.cache"): parses.append(1) or orig(self, path)


def parsed():
    parses.clear()
    COCODataset(img_path=str(imgs), json_file=str(jf), imgsz=320, augment=False)
    return bool(parses)


print("warm:", parsed(), "| rerun:", parsed())
a, b = sorted(imgs.glob("*.jpg"))[:2]
shutil.copy(b, a)  # overwrite an image in place with a different one
print("overwrite image in place -> parsed:", parsed())
extra = imgs / "extra.jpg"
shutil.copy(b, extra)
print("add an image file -> parsed:", parsed())
extra.unlink()
print("remove it -> parsed:", parsed())
