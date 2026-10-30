"""Check every claim in the coco-json-training cache note against the guide's own COCODataset code.

Usage: python verify_note.py <path to coco-json-training.md> <empty work dir>
"""

import json
import os
import platform
import re
import shutil
import sys
from pathlib import Path

import numpy as np
from PIL import Image

guide, work = Path(sys.argv[1]), Path(sys.argv[2])
shutil.rmtree(work, ignore_errors=True)
work.mkdir(parents=True)
os.environ["YOLO_CONFIG_DIR"] = str(work / "cfg")

# The guide's first python block is the COCODataset class, used verbatim
exec(re.findall(r"```python\n(.*?)```", guide.read_text(encoding="utf-8"), re.S)[0])

parses = []
_orig = COCODataset.cache_labels
COCODataset.cache_labels = lambda self, path=Path("./labels.cache"): parses.append(1) or _orig(self, path)


def make_img(p, seed):
    p.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(np.random.default_rng(seed).integers(0, 255, (48, 64, 3), dtype=np.uint8)).save(p)


def setup(sub):
    """4 listed images, the 4th missing; returns (img_dir, json_file, prefix)."""
    root = work / ("sub" if sub else "flat")
    imgs, pre = root / "images", ("sub/" if sub else "")
    names = [f"{pre}im{i}.jpg" for i in range(4)]
    for i, n in enumerate(names[:3]):
        make_img(imgs / n, i)
    coco = {
        "images": [{"id": i, "file_name": n, "width": 64, "height": 48} for i, n in enumerate(names)],
        "annotations": [
            {"id": i, "image_id": i, "category_id": 1, "bbox": [10.25, 10.25, 20.25, 20.25], "iscrowd": 0}
            for i in range(4)
        ],
        "categories": [{"id": 1, "name": "thing"}],
    }
    jf = root / "ann.json"
    jf.write_text(json.dumps(coco))
    return imgs, jf, pre


def load(imgs, jf):
    parses.clear()
    ds = COCODataset(img_path=str(imgs), json_file=str(jf), imgsz=64, augment=False)
    return bool(parses), len(ds.labels), round(float(ds.labels[0]["bboxes"][0][2]), 4)


rows = []


def check(claim, expect_parse, got):
    rows.append((claim, expect_parse, got[0], got[1], got[0] == expect_parse))


for sub in (False, True):
    imgs, jf, pre = setup(sub)
    where = "subfolder" if sub else "top level"
    load(imgs, jf)  # warm
    check(f"[{where}] rerun, nothing changed -> cache hit", False, load(imgs, jf))
    if not sub:
        s, st = jf.read_text(), jf.stat()
        jf.write_text(s.replace("20.25,", "30.25,", 1))  # same byte count
        assert jf.stat().st_size == st.st_size
        check("[JSON] same-size edit -> re-parse", True, load(imgs, jf))
        st = jf.stat()
        jf.write_text(jf.read_text().replace("30.25,", "40.25,", 1))
        os.utime(jf, ns=(st.st_atime_ns, st.st_mtime_ns))
        check("[JSON] edit + original mtime restored -> cache hit (stale)", False, load(imgs, jf))
    make_img(imgs / f"{pre}im0.jpg", 99)
    check(f"[{where}] replace an image in place -> cache hit", False, load(imgs, jf))
    make_img(imgs / f"{pre}im3.jpg", 3)
    check(f"[{where}] add the missing listed image -> {'cache hit' if sub else 're-parse'}", not sub, load(imgs, jf))
    (imgs / f"{pre}im3.jpg").unlink()
    check(f"[{where}] remove that image -> {'cache hit' if sub else 're-parse'}", not sub, load(imgs, jf))

print(f"{platform.system()} {platform.release()} | python {platform.python_version()}")
print(f"{'claim':<60} {'expect':<8} {'parsed':<7} {'images':<6} ok")
for claim, e, p, n, ok in rows:
    print(f"{claim:<60} {'parse' if e else 'hit':<8} {p!s:<7} {n:<6} {ok}")
print("ALL MATCH" if all(r[-1] for r in rows) else "MISMATCH")
