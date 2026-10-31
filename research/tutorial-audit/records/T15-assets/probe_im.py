from ultralytics import YOLO
for w, d, a in (("yolo26n.pt","coco8.yaml","box"),("yolo26n-seg.pt","coco8-seg.yaml","seg"),("yolo26n-pose.pt","coco8-pose.yaml","pose"),("yolo26n-obb.pt","dota8.yaml","box")):
    r = YOLO(w).val(data=d, imgsz=160, device="cpu", plots=False, verbose=False, workers=0)
    im = getattr(r, a).image_metrics
    k = next(iter(im), None)
    print(w, a, len(im), k, {x: round(v, 3) for x, v in im[k].items()} if k else None)
    if a in ("seg", "pose"): print("  box image_metrics too:", len(r.box.image_metrics))
