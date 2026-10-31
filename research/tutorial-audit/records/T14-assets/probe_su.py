import json, shutil, tempfile, traceback
from pathlib import Path
import cv2, numpy as np
from ultralytics.utils import ASSETS
W = Path(tempfile.mkdtemp()); print("W", W)
def t(name):
    def deco(f):
        try: print(f"[{name}]", f())
        except Exception as e: print(f"[{name}] EXC {type(e).__name__}: {str(e)[:200]}"); traceback.print_exc(limit=-2)
    return deco
@t("formats")
def _():
    from ultralytics.data.utils import IMG_FORMATS, VID_FORMATS
    di={'avif','bmp','dng','heic','heif','jp2','jpeg','jpg','mpo','png','tif','tiff','webp'}; dv={'asf','avi','gif','m4v','mkv','mov','mp4','mpeg','mpg','ts','wmv','webm'}
    return dict(img_extra=set(IMG_FORMATS)-di,img_missing=di-set(IMG_FORMATS),vid_extra=set(VID_FORMATS)-dv,vid_missing=dv-set(VID_FORMATS))
@t("make_div")
def _():
    from ultralytics.utils.ops import make_divisible
    return make_divisible(7,3),make_divisible(7,2)
@t("seg2box")
def _():
    from ultralytics.utils.ops import segments2boxes
    s=np.array([[805,392,797,400,812,402,808,714,808,392],[115,398,113,400,150,410,150,400,149,298],[267,412,265,413,300,420,300,413,299,412]],dtype=np.float32)
    r=segments2boxes([x.reshape(-1,2) for x in s]); return r.tolist(), r.dtype
@t("profile")
def _():
    from ultralytics.utils.ops import Profile
    with Profile() as dt: pass
    return str(dt)
@t("bboxes")
def _():
    from ultralytics.utils.instance import Bboxes
    b=Bboxes(bboxes=np.array([[22.878,231.27,804.98,756.83],[48.552,398.56,245.35,902.71]]),format="xyxy"); a=b.areas().tolist(); b.convert("xywh"); return a,b.bboxes.tolist()
@t("masks2seg binary?")
def _():
    from ultralytics.data.converter import convert_segment_masks_to_yolo_seg
    m=W/"m"; o=W/"o"; m.mkdir(); o.mkdir()
    a=np.zeros((100,100),np.uint8); a[10:40,10:40]=1; a[50:90,50:90]=255
    cv2.imwrite(str(m/"a.png"),a)
    b=np.zeros((100,100),np.uint8); b[10:40,10:40]=255; cv2.imwrite(str(m/"b.png"),b)
    convert_segment_masks_to_yolo_seg(str(m),str(o),classes=80)
    return {p.name:[l.split()[0] for l in p.read_text().splitlines()] for p in sorted(o.glob("*.txt"))}
@t("compress")
def _():
    from ultralytics.data.utils import compress_one_image
    f=W/"c.jpg"; shutil.copy(ASSETS/"bus.jpg",f); s0=f.stat().st_size; compress_one_image(f); im=cv2.imread(str(f))
    g=W/"small.jpg"; cv2.imwrite(str(g),np.random.randint(0,255,(100,200,3),np.uint8)); s1=g.stat().st_size; compress_one_image(g); im2=cv2.imread(str(g))
    return s0,f.stat().st_size,im.shape,"small",s1,g.stat().st_size,im2.shape
@t("polygon2mask")
def _():
    from ultralytics.data.utils import polygon2mask
    p=np.array([805,392,797,400,812,402,808,714,808,392]); m=polygon2mask((1080,810),[p],color=255,downsample_ratio=1); return m.shape,m.dtype,np.unique(m).tolist()
@t("autosplit")
def _():
    from ultralytics.data.split import autosplit
    d=W/"ds"/"images"; d.mkdir(parents=True)
    for i in range(10): shutil.copy(ASSETS/"bus.jpg",d/f"{i}.jpg")
    autosplit(path=str(d),weights=(0.9,0.1,0.0),annotated_only=False)
    return sorted(str(p.relative_to(W)) for p in W.rglob("autosplit*"))
@t("coco convert")
def _():
    from ultralytics.data.converter import convert_coco
    a=W/"coco"/"annotations"; a.mkdir(parents=True)
    J=dict(images=[dict(id=1,file_name="x.jpg",height=100,width=100)],annotations=[dict(id=1,image_id=1,category_id=1,bbox=[10,10,20,20],iscrowd=0,area=400,segmentation=[[10,10,30,10,30,30]])],categories=[dict(id=1,name="person")])
    (a/"instances_train2017.json").write_text(json.dumps(J))
    import os; os.chdir(W)
    convert_coco(str(a)+"/",use_segments=False,use_keypoints=False,cls91to80=True)
    return sorted(str(p.relative_to(W)) for p in W.glob("coco_converted*/**/*"))
@t("bbox2seg")
def _():
    from ultralytics.data.converter import yolo_bbox2segment
    d=W/"data"; (d/"images").mkdir(parents=True); (d/"labels").mkdir()
    shutil.copy(ASSETS/"bus.jpg",d/"images/001.jpg"); (d/"labels/001.txt").write_text("5 0.5 0.45 0.9 0.5\n")
    yolo_bbox2segment(im_dir=str(d/"images"),save_dir=None,sam_model="mobile_sam.pt",device="cpu")
    return sorted(str(p.relative_to(W)) for p in d.rglob("*") if p.is_file()), [len(l.split()) for l in next((d/"labels-segment").glob("*.txt")).read_text().splitlines()]
@t("visualize")
def _():
    from ultralytics.data.utils import visualize_image_annotations
    import matplotlib; matplotlib.use("Agg")
    f=W/"a.txt"; f.write_text("0 0.5 0.5 0.2 0.2\n")
    return visualize_image_annotations(str(ASSETS/"bus.jpg"),str(f),{0:"person"})
