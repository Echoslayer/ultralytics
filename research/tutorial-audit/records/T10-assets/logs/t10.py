import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path


if __name__ == "__main__":
    out = Path(sys.argv[1]).resolve()
    if len(sys.argv) == 2:
        root = Path.cwd()
        out.mkdir(parents=True, exist_ok=False)
        execution = {}
        for name, fmt in [("pytorch", "-"), ("onnx", "onnx")]:
            work = out / name
            work.mkdir()
            shutil.copy2(root / "yolo26n.pt", work / "yolo26n.pt")
            config = work / "config" / "Ultralytics"
            config.mkdir(parents=True)
            settings = json.loads((root / "config/Ultralytics/settings.json").read_text())
            settings["runs_dir"] = str(work / "runs")
            (config / "settings.json").write_text(json.dumps(settings))
            env = dict(os.environ, YOLO_CONFIG_DIR=str(work / "config"), YOLO_AUTOINSTALL="False")
            start = time.perf_counter()
            with (work / "run.log").open("w", encoding="utf-8") as log:
                result = subprocess.run([sys.executable, __file__, str(work), fmt], cwd=work, env=env,
                                        stdout=log, stderr=subprocess.STDOUT)
            execution[name] = {"exit_code": result.returncode, "seconds": time.perf_counter() - start}
            (out / "execution.json").write_text(json.dumps(execution, indent=2))
            assert result.returncode == 0, work / "run.log"
    else:
        import inspect
        from ultralytics.utils.benchmarks import benchmark

        (out / "installed-benchmark.py").write_text(inspect.getsource(benchmark), encoding="utf-8")
        result = benchmark(model=str(out / "yolo26n.pt"), data="coco8.yaml", imgsz=640,
                           device="cpu", format=sys.argv[2])
        result.write_csv(out / "results.csv")
        (out / "results.json").write_text(json.dumps(result.to_dicts(), indent=2), encoding="utf-8")
        assert result.height == 1
        assert result.row(0, named=True)["Status❔"] == "✅", result
