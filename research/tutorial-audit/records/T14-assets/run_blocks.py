"""Run each python fence of the given docs pages in its own process and scratch cwd. Prints one line per block."""

import re
import shutil
import subprocess
import sys
import textwrap
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

root, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
pages = sys.argv[3:]
py = str(Path(sys.executable))
fence = re.compile(r"^([ \t]*)```python[^\n]*\n(.*?)^\1```", re.S | re.M)
assets = root / "ultralytics/assets"
LIVE = re.compile(r"imshow|waitKey|VideoCapture\(0\)|streamlit|\.tune\(|coco\.yaml|imagenet|epochs=(?:[2-9]\d|\d{3,})|^\s*.*show=True", re.M)


def run(job):
    page, i, line, code = job
    d = out / page.replace("/", "_").replace(".md", "") / f"b{i:03d}"
    d.mkdir(parents=True, exist_ok=True)
    (d / "block.py").write_text(code, encoding="utf-8")
    if LIVE.search(code):
        return f"SKIP  {page}:{line} live/heavy"
    for n in ("bus.jpg", "zidane.jpg"):
        shutil.copy(assets / n, d / n)
    code2 = code.replace('"path/to/image.jpg"', '"bus.jpg"').replace("'path/to/image.jpg'", "'bus.jpg'")
    (d / "block.py").write_text(code2, encoding="utf-8")
    try:
        r = subprocess.run([py, "block.py"], cwd=d, capture_output=True, text=True, timeout=150)
    except subprocess.TimeoutExpired:
        return f"TIME  {page}:{line}"
    (d / "log.txt").write_text(r.stdout + r.stderr, encoding="utf-8")
    if r.returncode == 0:
        return f"OK    {page}:{line}"
    last = [x for x in r.stderr.strip().splitlines() if x.strip()]
    return f"FAIL  {page}:{line}  {last[-1][:170] if last else ''}"


jobs = []
for page in pages:
    text = (root / page).read_text(encoding="utf-8")
    for i, m in enumerate(fence.finditer(text)):
        jobs.append((page, i, text[: m.start()].count("\n") + 1, textwrap.dedent(m.group(2))))
print(len(jobs), "blocks", flush=True)
with ThreadPoolExecutor(5) as ex:
    for r in ex.map(run, jobs):
        print(r, flush=True)
