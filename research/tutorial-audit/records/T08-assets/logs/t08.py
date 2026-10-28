import json
import subprocess
import sys
import time
from pathlib import Path


def main():
    out = Path(sys.argv[1]).resolve()
    if len(sys.argv) == 2:
        out.mkdir(parents=True, exist_ok=False)
        start = time.perf_counter()
        with (out / "track.log").open("w", encoding="utf-8") as log:
            result = subprocess.run([sys.executable, __file__, str(out), "run"], stdout=log, stderr=subprocess.STDOUT)
        (out / "execution.json").write_text(json.dumps({"exit_code": result.returncode, "seconds": time.perf_counter() - start}, indent=2))
        assert result.returncode == 0, out / "track.log"
        return

    import cv2
    from ultralytics import YOLO

    report = {}
    for name, options in [("default", {}), ("bytetrack", {"tracker": "bytetrack.yaml"})]:
        model = YOLO(str(Path.cwd() / "yolo26n.pt"))
        frames = []
        # shortcut: repeated static frames validate plumbing only; use real motion for quality evaluation.
        for index, result in enumerate(model.track(source="t04/short.avi", stream=True, save=True, show=False,
                                                  device="cpu", project=str(out), name=name, **options)):
            boxes = result.boxes
            frames.append({"frame": index, "ids": boxes.id.int().tolist() if boxes.id is not None else [],
                           "classes": boxes.cls.int().tolist(), "xyxy": boxes.xyxy.tolist()})
            if index in (0, 9):
                assert cv2.imwrite(str(out / f"{name}-{index}.jpg"), result.plot())
        videos = list((out / name).glob("*.avi"))
        assert len(videos) == 1, videos
        capture = cv2.VideoCapture(str(videos[0]))
        fps = capture.get(cv2.CAP_PROP_FPS)
        decoded = 0
        while capture.read()[0]:
            decoded += 1
        capture.release()
        assert len(frames) == decoded == 10
        assert all(frame["ids"] for frame in frames)
        report[name] = {"tracker": model.predictor.args.tracker, "fps": fps, "decoded_frames": decoded, "frames": frames}
    (out / "results.json").write_text(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
