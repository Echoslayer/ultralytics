"""Run custom-trainer.md blocks for real: one epoch on coco8, imgsz 160, CPU."""
import re, subprocess, sys, textwrap
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
root, out = Path(sys.argv[1]), Path(sys.argv[2])
page = sys.argv[3]
text = (root / page).read_text()
fence = re.compile(r"^([ \t]*)```python[^\n]*\n(.*?)^\1```", re.S | re.M)
def run(j):
    line, code = j
    d = out / f"L{line}"; d.mkdir(parents=True, exist_ok=True)
    code = re.sub(r"epochs=\d+", "epochs=1", code).replace('data="custom.yaml"', 'data="coco8.yaml"')
    code = re.sub(r"(\.train\()", r"\1imgsz=160, device='cpu', workers=0, ", code) if "imgsz=" not in code else re.sub(r"imgsz=\d+", "imgsz=160", code)
    code = code.replace("coco.yaml", "coco8.yaml")
    (d / "block.py").write_text(code)
    try:
        r = subprocess.run([sys.executable, "block.py"], cwd=d, capture_output=True, text=True, timeout=240)
    except subprocess.TimeoutExpired:
        return f"TIME {page}:{line}"
    (d / "log.txt").write_text(r.stdout + r.stderr)
    tail = [x for x in r.stderr.strip().splitlines() if x.strip()]
    return f"{'OK  ' if r.returncode == 0 else 'FAIL'} {page}:{line}  {'' if r.returncode == 0 else tail[-1][:200]}"
jobs = [(text[: m.start()].count("\n") + 1, textwrap.dedent(m.group(2))) for m in fence.finditer(text)]
jobs = [j for j in jobs if ".train(" in j[1]]
with ThreadPoolExecutor(3) as ex:
    for r in ex.map(run, jobs): print(r, flush=True)
