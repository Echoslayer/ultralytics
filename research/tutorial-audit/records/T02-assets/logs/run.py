import subprocess, time, json, sys, platform
from pathlib import Path
import torch, ultralytics
root = Path.cwd()
out = root/'t02'
out.mkdir(exist_ok=True)
info = {'python': sys.version, 'platform': platform.platform(), 'torch': torch.__version__, 'ultralytics': ultralytics.__version__, 'import_path': ultralytics.__file__}
(root/'t02-environment.json').write_text(json.dumps(info, indent=2), encoding='utf-8')
summary = []
for name, conf in [('baseline', '0.25'), ('high-conf', '0.85')]:
    command = [str(root/'.venv/Scripts/yolo.exe'), 'detect', 'predict', 'model='+str(root/'yolo26n.pt'), 'source='+str(root/'bus.jpg'), 'project='+str(out), 'name='+name, 'conf='+conf, 'save_txt=True', 'save_conf=True']
    started = time.perf_counter()
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (out/(name+'.log')).write_bytes(result.stdout)
    record = {'name': name, 'conf': conf, 'command': command, 'exit_code': result.returncode, 'seconds': round(time.perf_counter()-started, 3)}
    labels = out/name/'labels/bus.txt'
    record['labels'] = labels.read_text().splitlines() if labels.exists() else None
    record['image_exists'] = (out/name/'bus.jpg').is_file()
    summary.append(record)
    print(json.dumps(record), flush=True)
    if result.returncode:
        break
(out/'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
