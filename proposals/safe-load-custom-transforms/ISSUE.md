# Issue 草稿：安全載入拒絕自訂分類轉換的模型

狀態：2026-10-29 草稿，尚未送出。下方英文本文可直接貼進 GitHub 的 Bug Report 範本。

## 送出前

1. **用最新版重跑。** 範本要求先 `pip install -U ultralytics` 再回報。本機驗證用的是研究分支的 8.4.191（`cfc8e272c`），不是 PyPI 最新版。在乾淨環境安裝最新版，把 `YOLO_CONFIG_DIR` 指到暫存目錄，跑下方 MRE；仍失敗才送出。
2. **貼上 `yolo checks` 的完整輸出**到 Environment 欄。
3. **再搜尋一次** `ULTRALYTICS_SAFE_LOAD`、`ClassifyLetterBox`、`safe_only`。2026-10-29 搜尋時，沒有找到同題 issue。
4. **AI 輔助聲明**比照 PR #26935 的做法（見第一章）。

## 範本欄位怎麼填

| 欄位 | 填法 |
| --- | --- |
| Title | `Safe load rejects classify models trained with the docs' custom transforms` |
| Search before asking | 勾選 |
| Component | `Predict` |
| Bug / Minimal Reproducible Example / Additional | 貼下方對應段落 |
| Environment | 最新版的 `yolo checks` 輸出 |
| Willing to submit a PR | 勾選，但等維護者選定方向再動手 |

## 寫法

刻意寫短、口語，只拋出現象和兩個可能方向，請維護者決定。不用粗體和長條列，不 @ 任何人。MRE 已在本機實跑，重現成功。

---

## Bug

If I train a classifier with the [custom transforms example](https://docs.ultralytics.com/tasks/classify/#custom-transforms), the resulting `best.pt` loads fine normally, but fails under `ULTRALYTICS_SAFE_LOAD=1`:

```
TypeError: ERROR ❌️ .../best.pt references types outside the supported Ultralytics checkpoint format. Use an official Ultralytics model, i.e. 'yolo predict model=yolo26n.pt'
```

The saved transforms reference `ClassifyLetterBox`, `ToPILImage` and `numpy.asarray`, which aren't in the safe-load allow-list. The error also reads a bit odd here, since this is a model trained by following the docs.

## Minimal Reproducible Example

```python
from pathlib import Path

import cv2
import numpy as np
import torch
import torchvision.transforms as T

from ultralytics import YOLO
from ultralytics.data.augment import ClassifyLetterBox
from ultralytics.data.dataset import ClassificationDataset
from ultralytics.models.yolo.classify import ClassificationTrainer
from ultralytics.nn.tasks import torch_safe_load

for split in ("train", "val"):
    for cls in ("a", "b"):
        Path(f"data/{split}/{cls}").mkdir(parents=True, exist_ok=True)
        cv2.imwrite(f"data/{split}/{cls}/0.png", np.full((64, 256, 3), 128, np.uint8))


class CustomizedDataset(ClassificationDataset):
    def __init__(self, root, args, augment=False, prefix="", names=None):
        super().__init__(root, args, augment, prefix, names)
        letterbox = T.Compose([np.asarray, ClassifyLetterBox(args.imgsz), T.ToPILImage()])
        self.torch_transforms = T.Compose([letterbox, T.ToTensor(), T.Normalize(mean=torch.tensor(0), std=torch.tensor(1))])


class CustomizedTrainer(ClassificationTrainer):
    def build_dataset(self, img_path, mode="train", batch=None):
        return CustomizedDataset(img_path, self.args, mode == "train", names=self.data["names"])


model = YOLO("yolo26n-cls.yaml")
model.train(data="data", trainer=CustomizedTrainer, epochs=1, imgsz=64, batch=2, workers=0)

torch_safe_load(model.trainer.best)  # OK
torch_safe_load(model.trainer.best, safe_only=True)  # TypeError
```

## Additional

Came across this while looking at #26707. Not sure which way you'd prefer: allow these transforms (similar to #26777), or just name the rejected type in the error. Happy to send a PR either way.
