# #26707 延伸提案：安全載入模式無法載入文件範例訓練出的分類模型

狀態：2026-10-29 研究草稿，優先度低。尚未開 issue 或 PR。建議**先開 issue 附重現步驟**，不要直接送 PR，因為修改會碰到安全載入的允許清單。可直接貼上的 issue 草稿見 [ISSUE.md](ISSUE.md)。

## 問題是什麼

照官方文件 `docs/en/tasks/classify.md` 的「Custom transforms」範例訓練分類模型：

- **預設載入：正常。** 推論時沿用 letterbox，保留整張圖片。
- **開啟 `ULTRALYTICS_SAFE_LOAD=1`：載入失敗。** 錯誤訊息是：

```text
TypeError: ERROR ❌️ best.pt references types outside the supported Ultralytics checkpoint format.
Use an official Ultralytics model, i.e. 'yolo predict model=yolo26n.pt'
```

這則訊息要使用者改用官方模型，但使用者訓練的是自己的模型，而且完全照文件操作。訊息沒有說出是哪個型別被擋下。

## 原因

訓練時，分類 trainer 會把驗證轉換存進模型（`classify/train.py`），推論再沿用。安全載入模式會對 checkpoint 中的每個 global 檢查允許清單（`nn/tasks.py` 的 `_SafeLoad`）。分類轉換只允許 `Compose`、`Normalize`、`Resize`、`CenterCrop`、`ToTensor`。

用 `torch.serialization.get_unsafe_globals_in_checkpoint` 檢查實驗產生的 `best.pt`，扣掉載入時會動態註冊的模型層後，只缺三個：

| 缺少的 global | 來自文件範例的哪一段 |
| --- | --- |
| `ultralytics.data.augment.ClassifyLetterBox` | `ClassifyLetterBox(args.imgsz)` |
| `torchvision.transforms.transforms.ToPILImage` | `T.ToPILImage()` |
| `numpy.asarray` | `np.asarray`（把 PIL 圖轉成陣列） |

上游 main `922563eab` 的允許清單與錯誤訊息都和實驗版本相同。

## 有前例

[PR #26777](https://github.com/ultralytics/ultralytics/pull/26777) 已合併：蒸餾續訓在安全載入下失敗，修正方式是把 `ultralytics.nn.distill_model` 加入允許規則。所以維護者接受「讓官方支援的工作流程能在安全載入下運作」這類修改。

## 可選的修正方向

| 方向 | 修改 | 優點 | 疑慮 |
| --- | --- | --- | --- |
| A. 擴充允許清單 | 在分類轉換那一行加入 `ToPILImage`、`ClassifyLetterBox`；`numpy.asarray` 另外處理 | 文件範例不用改；與 #26777 同一種修法 | `numpy.asarray` 是函式，不是類別，維護者可能不願意放行 |
| B. 調整文件範例 | 讓範例不再序列化 `np.asarray`，例如用小型轉換類別包住 | 不必放行函式 | 仍需要 A 的兩個類別；文件會變長 |
| C. 只改錯誤訊息 | 失敗時列出被擋下的 global 名稱 | 修改最小、沒有安全疑慮 | 問題還在，只是比較好排查 |

**本書建議：issue 裡附上重現步驟與 A／C 兩案，由維護者選擇。** 安全相關修改由維護者決定範圍，比較不會白做。

## 重現步驟

```powershell
$env:YOLO_CONFIG_DIR = Join-Path $env:TEMP 'yolo-cfg-26707'
python -I research/contributing/analysis/cls_letterbox_26707.py $env:TEMP\cls26707
# 結果在 <輸出目錄>/report.json 的 safe_load_predict 欄位
```

腳本會產生四角有色塊的合成圖片，照文件範例訓練 1 輪（CPU、64 像素），分別用預設模式與安全載入模式推論。2026-10-29 的結果見 [cls-letterbox-26707.json](../../research/contributing/docs/assets/cls-letterbox-26707.json)；研究卡見[第四章](../../research/contributing/docs/roadmap.md)。

## 送出前要做的事

1. 在官方最新 main 重跑，確認問題還在。
2. 搜尋 `ULTRALYTICS_SAFE_LOAD`、`ClassifyLetterBox` 相關議題與 PR。2026-10-29 搜尋時，沒有找到同題討論。
3. 先開 issue；維護者選定方向後，再依[第一章](../../research/contributing/docs/contribution-workflow.md)開乾淨分支送 PR。

## 為什麼優先度低

安全載入是選用功能，預設路徑完全正常。同時使用安全載入與自訂分類轉換的使用者可能不多。

---

# #26707 follow-up: restricted loading rejects classifiers trained with the documented custom transforms

Status: research draft, low priority, 2026-10-29. No issue or PR yet. Recommended path: **open an issue with a reproduction first**, because any fix touches the restricted-load allow-list.

## Problem

Train a classifier with the "Custom transforms" example in `docs/en/tasks/classify.md`:

- **Default loading works.** Prediction reuses the letterbox transform and keeps the full frame.
- **With `ULTRALYTICS_SAFE_LOAD=1`, loading fails:**

```text
TypeError: ERROR ❌️ best.pt references types outside the supported Ultralytics checkpoint format.
Use an official Ultralytics model, i.e. 'yolo predict model=yolo26n.pt'
```

The message tells users to switch to an official model, although they trained their own model by following the docs. It does not name the rejected type.

## Cause

The classification trainer stores the validation transforms on the model (`classify/train.py`), and prediction reuses them. Restricted loading checks every checkpoint global against `_SafeLoad` in `nn/tasks.py`. For classification transforms, only `Compose`, `Normalize`, `Resize`, `CenterCrop`, and `ToTensor` are allowed.

`torch.serialization.get_unsafe_globals_in_checkpoint` on the trained `best.pt`, after excluding model layers registered dynamically at load time, shows three missing globals:

| Missing global | Source in the docs example |
| --- | --- |
| `ultralytics.data.augment.ClassifyLetterBox` | `ClassifyLetterBox(args.imgsz)` |
| `torchvision.transforms.transforms.ToPILImage` | `T.ToPILImage()` |
| `numpy.asarray` | `np.asarray` |

Upstream main `922563eab` has the same allow-list and message.

## Precedent

Merged [PR #26777](https://github.com/ultralytics/ultralytics/pull/26777) fixed distillation resume under restricted loading by extending the allow-list rule to `ultralytics.nn.distill_model`.

## Options

| Option | Change | Pros | Concerns |
| --- | --- | --- | --- |
| A. Extend allow-list | Add `ToPILImage` and `ClassifyLetterBox` to the classification transform entries; handle `numpy.asarray` separately | Docs unchanged; same pattern as #26777 | `numpy.asarray` is a function, not a class |
| B. Adjust docs example | Avoid serializing `np.asarray`, e.g. wrap it in a small transform class | No function in the allow-list | Still needs A's two classes; longer docs |
| C. Improve error only | Name the rejected global when loading fails | Smallest change, no security trade-off | Problem remains, only easier to diagnose |

**Recommendation: file an issue with the reproduction and options A and C, and let maintainers choose.**

## Reproduction

```powershell
$env:YOLO_CONFIG_DIR = Join-Path $env:TEMP 'yolo-cfg-26707'
python -I research/contributing/analysis/cls_letterbox_26707.py $env:TEMP\cls26707
# see safe_load_predict in <output>/report.json
```

The script generates synthetic images with colored corners, trains one epoch with the docs example (CPU, 64 px), and predicts with default and restricted loading. Results from 2026-10-29: [cls-letterbox-26707.json](../../research/contributing/docs/assets/cls-letterbox-26707.json).

## Before submitting

1. Rerun on the latest upstream main.
2. Search issues and PRs for `ULTRALYTICS_SAFE_LOAD` and `ClassifyLetterBox`; none matched on 2026-10-29.
3. Open the issue first; open a PR only after maintainers pick a direction.

## Why low priority

Restricted loading is opt-in, and the default path works. Few users likely combine it with custom classification transforms.
