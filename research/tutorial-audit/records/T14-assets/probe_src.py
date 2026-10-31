import csv, shutil, tempfile
from pathlib import Path
from ultralytics import YOLO
from ultralytics.data.build import load_inference_source
d = Path(tempfile.mkdtemp()); a = Path("um/ultralytics/assets").resolve()
(d/"sub").mkdir()
for i in range(3): shutil.copy(a/"bus.jpg", d/f"{i}.jpg")
shutil.copy(a/"zidane.jpg", d/"sub"/"z.jpg")
(d/"abs.txt").write_text("\n".join(str(d/f"{i}.jpg") for i in (2,0,1)))
(d/"rel.txt").write_text("./0.jpg\n./sub/z.jpg\n")
(d/"bare.txt").write_text("0.jpg\nsub/z.jpg\n")
(d/"c.csv").write_text("source\n"+"\n".join(str(d/f"{i}.jpg") for i in range(3)))
import os; os.chdir(tempfile.mkdtemp())
for name, s in [("abs.txt", str(d/"abs.txt")), ("csv", str(d/"c.csv")), ("glob", str(d/"*.jpg")), ("dir", str(d)), ("list", [str(d/f"{i}.jpg") for i in range(3)]),
                ("rel ./ txt", str(d/"rel.txt")), ("bare txt", str(d/"bare.txt"))]:
    try:
        ds = load_inference_source(s, batch=2)
        sizes = [len(b[0]) for b in ds]
        print(f"{name:12} {type(ds).__name__:22} bs={getattr(ds,'bs',None)} batches={sizes}")
    except Exception as e:
        print(f"{name:12} {type(e).__name__}: {str(e)[:110]}")
