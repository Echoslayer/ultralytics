import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

root = Path.cwd()
out = Path(sys.argv[1]).resolve()
out.mkdir(parents=True, exist_ok=False)
env = dict(os.environ, YOLO_CONFIG_DIR=str(out / "config"), PYTHONIOENCODING="utf-8")
keys = ["datasets_dir", "weights_dir", "runs_dir", "tensorboard"]
values = {k: str(out / k) for k in keys[:3]}
values["tensorboard"] = False
for key in keys[:3]:
    Path(values[key]).mkdir()
shutil.copy2(root / "yolo26n.pt", Path(values["weights_dir"]) / "yolo26n.pt")
steps = []

def run(name, args):
    start = time.perf_counter()
    p = subprocess.run(args, cwd=out, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8")
    (out / f"{name}.log").write_text(p.stdout, encoding="utf-8")
    steps.append({"name": name, "exit": p.returncode, "seconds": time.perf_counter() - start})
    assert p.returncode == 0, p.stdout

def python(name, code):
    run(name, [sys.executable, "-c", code])

python("update", f"from ultralytics import settings; settings.update({values!r}); print({{k:settings[k] for k in {keys!r}}})")
python("verify", f"from ultralytics import settings; assert all(settings[k]==v for k,v in {values!r}.items()); print('PASS persisted settings')")
yolo = str(Path(sys.executable).with_name("yolo.exe"))
run("cli-update", [yolo, "settings", "tensorboard=True"])
python("cli-verify", "from ultralytics import settings; assert settings['tensorboard'] is True; print('PASS CLI persisted')")
python("paths", f'''
import inspect,json
from pathlib import Path
from ultralytics import YOLO,settings
from ultralytics.utils.downloads import attempt_download_asset
from ultralytics.utils import SETTINGS_FILE
from ultralytics.data.utils import check_det_dataset
out=Path.cwd()
fallback=Path(attempt_download_asset('yolo26n.pt')).resolve()
assert fallback == Path(settings['weights_dir'])/'yolo26n.pt'
model=YOLO('yolo26n.pt')
r=model({str(root / 'bus.jpg')!r},device='cpu',save=True,name='settings-default')[0]
default=Path(r.save_dir).resolve()
assert default == Path(settings['runs_dir'])/'detect/settings-default'
assert (default/'bus.jpg').exists()
r=model({str(root / 'bus.jpg')!r},device='cpu',save=True,project=out/'explicit-project',name='override')[0]
override=Path(r.save_dir).resolve()
assert override == out/'explicit-project/override'
assert (override/'bus.jpg').exists()
dataset=Path(settings['datasets_dir'])/'tiny'
(dataset/'images').mkdir(parents=True)
import shutil
shutil.copy2({str(root / 'bus.jpg')!r},dataset/'images/bus.jpg')
yaml=out/'tiny.yaml'
yaml.write_text('path: tiny\\ntrain: images\\nval: images\\nnames: [person]\\n')
data=check_det_dataset(str(yaml),autodownload=False)
assert Path(data['val']) == dataset/'images'
shutil.copy2(fallback,out/'yolo26n.pt')
cwd=Path(attempt_download_asset('yolo26n.pt')).resolve()
assert cwd == out/'yolo26n.pt'
report={{'settings_file':str(SETTINGS_FILE),'settings':{{k:settings[k] for k in {keys!r}}},'fallback':str(fallback),'cwd_precedence':str(cwd),'default_output':str(default),'project_override':str(override),'dataset_val':data['val'],'boxes':len(r.boxes)}}
(out/'results.json').write_text(json.dumps(report,indent=2))
(out/'download-owner.py').write_text(inspect.getsource(attempt_download_asset),encoding='utf-8')
print(json.dumps(report,indent=2))
''')
run("cli-reset", [yolo, "settings", "reset"])
python("reset-verify", f"from ultralytics import settings; assert settings['runs_dir']!={values['runs_dir']!r}; print('PASS CLI reset')")
python("python-reset", f"from ultralytics import settings; settings.update({values!r}); settings.reset(); assert settings['runs_dir']!={values['runs_dir']!r}; print('PASS Python reset')")
python("reset-reopen", f"from ultralytics import settings; assert settings['runs_dir']!={values['runs_dir']!r}; print('PASS reset persisted')")
(out / "execution.json").write_text(json.dumps(steps, indent=2), encoding="utf-8")
print(json.dumps(steps, indent=2))
