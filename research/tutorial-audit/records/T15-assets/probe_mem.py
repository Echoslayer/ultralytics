"""Measure real memory of endless sources without stream=True. Modes: screen, cam (fake camera), cam_ends (camera that stops)."""

import subprocess
import sys
import time

import cv2
import numpy as np

from ultralytics import YOLO


class FakeCam:
    """Stand-in for cv2.VideoCapture: noise frames at about 30 FPS, so the real LoadStreams runs without a camera."""

    limit = None

    def __init__(self, source):
        print("VideoCapture opened with", repr(source), flush=True)
        self.n = 0

    def isOpened(self):
        return self.limit is None or self.n < self.limit

    def get(self, prop):
        return {cv2.CAP_PROP_FRAME_WIDTH: 640, cv2.CAP_PROP_FRAME_HEIGHT: 480, cv2.CAP_PROP_FPS: 30}.get(prop, 0)

    def read(self):
        return True, np.random.randint(0, 255, (480, 640, 3), np.uint8)

    def grab(self):
        time.sleep(1 / 30)
        self.n += 1
        return True

    def retrieve(self):
        return self.read()

    def release(self):
        pass


def child(mode):
    n = [0, 0]
    if mode.startswith("cam"):
        FakeCam.limit = 60 if mode == "cam_ends" else None
        cv2.VideoCapture = FakeCam
    model = YOLO("yolo26n.pt")

    def count(p):
        n[0] += 1
        n[1] += p.results[0].orig_img.nbytes
        if n[0] % 100 == 0:
            print(f"frames={n[0]} retained_orig_img={n[1] // 2**20} MB", flush=True)

    model.add_callback("on_predict_batch_end", count)
    results = model.predict(source="screen" if mode == "screen" else "0", verbose=False)  # the docs calls
    print("RETURNED", len(results), flush=True)


def footprint(pid):
    """Return (rss MB, physical footprint text): RSS leaves out pages macOS has compressed, the footprint does not."""
    rss = subprocess.run(["ps", "-o", "rss=", "-p", str(pid)], capture_output=True, text=True).stdout.strip()
    top = subprocess.run(["top", "-l", "1", "-pid", str(pid), "-stats", "mem"], capture_output=True, text=True).stdout
    return int(rss or 0) // 1024, top.strip().splitlines()[-1].strip()


if __name__ == "__main__":
    if len(sys.argv) > 2:
        child(sys.argv[2])
        sys.exit()
    mode, limit = sys.argv[1], 60
    log = open(f"{mode}.child.log", "w")
    p = subprocess.Popen([sys.executable, "-u", __file__, "x", mode], stdout=log, stderr=subprocess.STDOUT)
    t0 = time.time()
    while p.poll() is None and time.time() - t0 < limit:
        time.sleep(15)
        if p.poll() is None:
            rss, fp = footprint(p.pid)
            print(f"{mode} t={time.time() - t0:.0f}s rss={rss} MB footprint={fp}", flush=True)
    returned = p.poll() is not None
    p.kill()
    log.close()
    text = open(f"{mode}.child.log").read()
    print(mode, "exited by itself:", returned, "| RETURNED line:", [x for x in text.splitlines() if x.startswith("RETURNED")])
    print(mode, [x for x in text.splitlines() if x.startswith(("VideoCapture", "frames="))][-2:])
