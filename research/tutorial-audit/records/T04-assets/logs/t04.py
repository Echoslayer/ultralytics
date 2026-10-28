import json
import shutil
import sys
import time
from pathlib import Path
from types import GeneratorType

import cv2
import ultralytics
from ultralytics import YOLO

root = Path.cwd()
out = Path(sys.argv[1]).resolve()
out.mkdir(parents=True, exist_ok=False)
images = out / "input"
images.mkdir()
shutil.copy2(root / "bus.jpg", images / "bus.jpg")
shutil.copy2(Path(ultralytics.__file__).parent / "assets/zidane.jpg", images / "zidane.jpg")
frame = cv2.resize(cv2.imread(str(images / "bus.jpg")), (406, 540))
video = out / "short.avi"
writer = cv2.VideoWriter(str(video), cv2.VideoWriter_fourcc(*"MJPG"), 5, (406, 540))
assert writer.isOpened(), "Cannot create MJPG input"
for _ in range(10):
    writer.write(frame)
writer.release()
model = YOLO(root / "yolo26n.pt")
report = {"version": ultralytics.__version__, "cases": {}}
for name, source, stream, expected in [
    ("single", images / "bus.jpg", False, 1),
    ("folder", images, False, 2),
    ("video_list", video, False, 10),
    ("video_stream", video, True, 10),
]:
    start = time.perf_counter()
    results = model(source, stream=stream, device="cpu", conf=0.25, save=True, project=out, name=name)
    before = (out / name).exists()
    assert isinstance(results, GeneratorType if stream else list)
    if stream:
        assert not before, "Prediction output created before iteration"
    rows = []
    for i, result in enumerate(results):
        rows.append({"index": i, "file": Path(result.path).name, "shape": list(result.orig_shape),
                     "boxes": result.boxes.data.cpu().tolist()})
        if i == 0:
            result.save(out / f"{name}-first.jpg")
    assert len(rows) == expected, (name, len(rows))
    case = {"type": type(results).__name__, "output_exists_before_iteration": before,
            "seconds": time.perf_counter() - start, "rows": rows}
    if name.startswith("video"):
        files = list((out / name).glob("*.avi")) + list((out / name).glob("*.mp4"))
        assert len(files) == 1, files
        cap = cv2.VideoCapture(str(files[0]))
        assert cap.isOpened()
        fps = cap.get(cv2.CAP_PROP_FPS)
        count = 0
        while True:
            ok, decoded = cap.read()
            if not ok:
                break
            count += 1
        cap.release()
        assert count == expected, (name, count)
        case["saved_video"] = {"file": files[0].name, "decoded_frames": count, "fps": fps}
    report["cases"][name] = case
assert report["cases"]["video_list"]["rows"] == report["cases"]["video_stream"]["rows"]
(out / "results.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print("PASS: source counts, lazy iteration, list/stream equality, saved video decoding")
