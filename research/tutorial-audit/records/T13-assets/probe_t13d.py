"""T13d: images in a subfolder (file_name 'sub/x.jpg'): does adding a missing image later refresh the cache?"""

import json
import os
import shutil
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "t13out"
os.environ["YOLO_CONFIG_DIR"] = str(OUT / "cfg")
src = (HERE / "coco_full.py").read_text().splitlines()
exec("\n".join(src[:-2]))

base = OUT / "my_dataset"
root = OUT / "sub_case"
shutil.rmtree(root, ignore_errors=True)
imgs = root / "images" / "train"
(imgs / "sub").mkdir(parents=True)
coco = json.loads((base / "annotations" / "instances_train.json").read_text())
for im in coco["images"]:
    im["file_name"] = "sub/" + im["file_name"]
jf = root / "instances_train.json"
jf.write_text(json.dumps(coco))
names = [Path(im["file_name"]).name for im in coco["images"]]
for n in names[:3]:  # last image not copied yet
    shutil.copy(base / "images" / "train" / n, imgs / "sub" / n)


def build():
    ds = COCODataset(img_path=str(imgs), json_file=str(jf), imgsz=320, augment=False)
    return len(ds.labels)


print("JSON lists", len(names), "images; 3 present ->", build(), "images used")
m_top = imgs.stat().st_mtime_ns
shutil.copy(base / "images" / "train" / names[3], imgs / "sub" / names[3])
print("added the 4th image into sub/; top folder mtime changed =", imgs.stat().st_mtime_ns != m_top)
print("rerun ->", build(), "images used")
jf.with_suffix(".cache").unlink()
print("after deleting .cache ->", build(), "images used")
