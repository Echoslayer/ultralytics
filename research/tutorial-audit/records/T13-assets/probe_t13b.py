"""T13b: why did the cache miss on an unedited rerun? Rebuild twice and print the reason."""

import os
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "t13out"
os.environ["YOLO_CONFIG_DIR"] = str(OUT / "cfg")
src = (HERE / "coco_full.py").read_text().splitlines()
exec("\n".join(src[:-2]))
from ultralytics.data.utils import load_dataset_cache_file  # noqa: E402

root = OUT / "my_dataset"
jf = root / "annotations" / "instances_train.json"
for run in (1, 2):
    ds = COCODataset(img_path=str(root / "images" / "train"), json_file=str(jf), imgsz=320, augment=False)
    c = load_dataset_cache_file(jf.with_suffix(".cache"))
    print(f"run {run}: img_path={ds.img_path!r} labels={len(ds.labels)} cache_hash_matches={c['hash'] == get_hash([str(jf), str(ds.img_path)])}")

# Same-size edit (the guide's warning says this leaves the stale cache in place)
parses = []
orig = COCODataset.cache_labels
COCODataset.cache_labels = lambda self, path=Path("./labels.cache"): parses.append(1) or orig(self, path)


def first_w():
    parses.clear()
    ds = COCODataset(img_path=str(root / "images" / "train"), json_file=str(jf), imgsz=320, augment=False)
    return round(float(ds.labels[0]["bboxes"][0][2]), 4), bool(parses)


print("before edit: (w, parsed) =", first_w())
text, st = jf.read_text(), jf.stat()
edited = text.replace("211.59", "311.59", 1)  # probe_t13 already changed 611.59 -> 211.59
assert len(edited) == len(text) and edited != text
jf.write_text(edited)
print(f"same-size edit: size {st.st_size} -> {jf.stat().st_size}, mtime changed = {jf.stat().st_mtime_ns != st.st_mtime_ns}")
print("after edit: (w, parsed) =", first_w())

# Same edit again, but restore the old mtime (e.g. a tool that preserves timestamps)
st = jf.stat()
jf.write_text(edited.replace("311.59", "411.59", 1))
os.utime(jf, ns=(st.st_atime_ns, st.st_mtime_ns))
print("edit with mtime restored: (w, parsed) =", first_w())
