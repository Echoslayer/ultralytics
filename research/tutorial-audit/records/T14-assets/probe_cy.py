import json, tempfile, os
from pathlib import Path
os.chdir(tempfile.mkdtemp())
from ultralytics.data.converter import convert_coco
def mk(root, start):
    a=Path(root)/"annotations"; a.mkdir(parents=True)
    J=dict(images=[dict(id=1,file_name="a.jpg",height=100,width=100),dict(id=2,file_name="b.jpg",height=100,width=100)],
      annotations=[dict(id=1,image_id=1,category_id=start,bbox=[10,10,20,20],iscrowd=0,area=400,segmentation=[[10,10,30,10,30,30]]),dict(id=2,image_id=1,category_id=start+1,bbox=[40,40,20,20],iscrowd=0,area=400,segmentation=[[40,40,60,40,60,60]])],
      categories=[dict(id=start,name="x"),dict(id=start+1,name="y")])
    (a/"instances_train.json").write_text(json.dumps(J)); return a
def show(d): return {str(p.relative_to(d)):p.read_text().strip().replace("\n"," | ") for p in sorted(Path(d).rglob("*.txt"))}
for start,kw in [(1,dict(cls91to80=False)),(0,dict(cls91to80=False)),(1,dict()),(0,dict())]:
    r=f"ds{start}{bool(kw)}"; a=mk(r,start)
    try:
        convert_coco(labels_dir=str(a)+"/",save_dir=f"{r}/converted/",**kw); print(start,kw,show(f"{r}/converted"))
    except Exception as e: print(start,kw,"EXC",type(e).__name__,e)
convert_coco(labels_dir="ds1True/annotations/",save_dir="ds1True/converted/",cls91to80=False); print(sorted(p.name for p in Path("ds1True").iterdir()))
