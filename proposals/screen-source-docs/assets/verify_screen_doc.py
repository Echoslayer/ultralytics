"""Run the fixed screenshot example from predict.md as written and check that it returns."""

import re
import subprocess
import sys
import textwrap
import time
from pathlib import Path

text = Path(sys.argv[1]).read_text(encoding="utf-8")
tab = text[text.index('=== "screenshot"') :]
code = textwrap.dedent(re.search(r"```python\n(.*?)^\s*```", tab, re.S | re.M).group(1))
print(code)
Path("screen_block.py").write_text(code, encoding="utf-8")
t0 = time.time()
r = subprocess.run([sys.executable, "screen_block.py"], capture_output=True, text=True, timeout=60)
print(f"exit={r.returncode} seconds={time.time() - t0:.1f} printed_boxes={'cls: tensor' in r.stdout or 'ultralytics.engine.results.Boxes' in r.stdout}")
print("stream warning shown:", "accumulate in RAM" in r.stdout + r.stderr)
assert r.returncode == 0
