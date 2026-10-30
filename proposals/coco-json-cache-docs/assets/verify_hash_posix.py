"""Stdlib-only: does get_hash([json, img_dir]) change for each case in the cache note? (cache hit <=> hash unchanged)

Usage: python3 verify_hash_posix.py <ultralytics/data/utils.py> <empty work dir>
"""

import ast
import os
import platform
import shutil
import sys
import time
from pathlib import Path

src = Path(sys.argv[1]).read_text(encoding="utf-8")
fn = next(n for n in ast.parse(src).body if isinstance(n, ast.FunctionDef) and n.name == "get_hash")
ns = {"os": os}
exec(ast.get_source_segment(src, fn), ns)  # get_hash verbatim from the repo
get_hash = ns["get_hash"]

work = Path(sys.argv[2])
GAP = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0  # seconds between steps
shutil.rmtree(work, ignore_errors=True)
rows = []
for sub in (False, True):
    root = work / ("sub" if sub else "flat")
    imgs = root / "images"
    d = imgs / "sub" if sub else imgs
    d.mkdir(parents=True)
    for i in range(3):
        (d / f"im{i}.jpg").write_bytes(bytes([i]) * 100)
    jf = root / "ann.json"
    jf.write_text('{"bbox": [20.25]}')
    key = lambda: get_hash([str(jf), str(imgs)])  # noqa: E731
    where = "subfolder" if sub else "top level"

    def step(claim, expect_change, action):
        time.sleep(GAP)
        before = key()
        action()
        changed = key() != before
        rows.append((f"[{where}] {claim}", expect_change, changed))

    if not sub:

        def same_size_edit():
            jf.write_text('{"bbox": [30.25]}')

        def edit_restore_mtime():
            st = jf.stat()
            jf.write_text('{"bbox": [40.25]}')
            os.utime(jf, ns=(st.st_atime_ns, st.st_mtime_ns))

        step("JSON same-size edit", True, same_size_edit)
        step("JSON edit + mtime restored", False, edit_restore_mtime)
    step("replace an image in place", False, lambda: (d / "im0.jpg").write_bytes(b"\x09" * 100))
    step("add an image", not sub, lambda: (d / "im3.jpg").write_bytes(b"\x03" * 100))
    step("remove that image", not sub, lambda: (d / "im3.jpg").unlink())

print(f"{platform.system()} {platform.release()} | python {platform.python_version()} | work dir {work} | gap {GAP}s")
print(f"{'case':<42} {'expect':<10} {'observed':<10} ok")
for c, e, o in rows:
    f = lambda x: "rebuild" if x else "cache hit"  # noqa: E731
    print(f"{c:<42} {f(e):<10} {f(o):<10} {e == o}")
print("ALL MATCH" if all(e == o for _, e, o in rows) else "MISMATCH")
