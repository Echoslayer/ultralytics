import time
from ultralytics import YOLO
m = YOLO("yolo26n.pt"); n=[0]; t0=time.time()
def c(p):
    n[0]+=1
    if n[0] in (1,10,50,100,200,300,500,800): print(f"frame {n[0]} t={time.time()-t0:.1f}", flush=True)
m.add_callback("on_predict_batch_end", c)
m("screen", verbose=False)
