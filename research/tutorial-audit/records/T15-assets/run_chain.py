"""Run a page's python blocks in one shared namespace, in order, continuing after failures."""
import contextlib, io, os, re, shutil, signal, sys, textwrap, traceback
from pathlib import Path

root, page = Path(sys.argv[1]), sys.argv[2]
text = (root / page).read_text()
fence = re.compile(r"^([ \t]*)```python[^\n]*\n(.*?)^\1```", re.S | re.M)
LIVE = re.compile(r"imshow|waitKey|VideoCapture\(0\)|streamlit|\.tune\(|\.show\(|show=True|source=0")
for n in ("bus.jpg", "zidane.jpg"):
    shutil.copy(root / "ultralytics/assets" / n, n)
ns = {"__name__": "__main__"}
class T(Exception): pass
signal.signal(signal.SIGALRM, lambda *a: (_ for _ in ()).throw(T()))
for m in fence.finditer(text):
    line = text[: m.start()].count("\n") + 1
    code = textwrap.dedent(m.group(2))
    if LIVE.search(code):
        print(f"SKIP {line}", flush=True); continue
    code = re.sub(r"epochs=\d+", "epochs=1", code).replace("path/to/image.jpg", "bus.jpg").replace("coco.yaml", "coco8.yaml")
    code = re.sub(r"imgsz=\d+", "imgsz=160", code)
    signal.alarm(120)
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            exec(compile(code, f"{page}:{line}", "exec"), ns)
        print(f"OK   {line}", flush=True)
    except BaseException as e:
        print(f"FAIL {line} {type(e).__name__}: {str(e)[:170]}", flush=True)
    signal.alarm(0)
