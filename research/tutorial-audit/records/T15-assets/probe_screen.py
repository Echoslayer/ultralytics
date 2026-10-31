"""Run the predict.md screenshot example under a time limit and report whether it returns."""

import subprocess
import sys
import time

from ultralytics import YOLO

LIMIT = 90

if len(sys.argv) > 1:  # the docs example, plus a frame counter
    model = YOLO("yolo26n.pt")
    n = [0]

    def count(predictor):
        n[0] += 1
        if n[0] % 100 == 0:
            print(f"frames={n[0]}", flush=True)

    model.add_callback("on_predict_batch_end", count)
    source = "screen"
    results = model(source, verbose=False)
    print("RETURNED", len(results), flush=True)
    sys.exit()

n, t0 = 0, time.time()
gen = YOLO("yolo26n.pt")("screen", stream=True, verbose=False)
for r in gen:
    n += 1
    shape = r.orig_img.shape
    if time.time() - t0 > 20:
        break
gen.close()
print(f"stream=True: {n} frames in {time.time() - t0:.0f}s, shape {shape}, stopped by the caller")

p = subprocess.Popen([sys.executable, __file__, "docs"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
for _ in range(LIMIT // 30):
    time.sleep(30)
    rss = subprocess.run(["ps", "-o", "rss=", "-p", str(p.pid)], capture_output=True, text=True).stdout.strip()
    print(f"docs example t={int(time.time() - t0)}s rss={int(rss or 0) // 1024} MB alive={p.poll() is None}", flush=True)
p.kill()
out = p.communicate()[0]
print("returned to caller:", "RETURNED" in out)
print("stream warning shown:", "accumulate in RAM" in out)
