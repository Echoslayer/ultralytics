# T07 提案：說明 `metrics.box.maps` 對未評估類別的填值

狀態：2026-10-29 研究草稿。尚未建立分支、修改上游或開 PR。

## 為什麼值得做

文件寫 `metrics.box.maps` 是「每個類別的 mAP50-95」。實際上，驗證集沒有出現的類別，會被填入**整體 mAP**，不是該類別的成績。T07 在 COCO8 驗證時，80 個值中只有 6 個類別真的評估過，其餘 74 個都顯示 0.695148（整體 mAP）。

讀者若直接拿 `maps` 找「表現最差的類別」，會把填值誤當成實測。

- 證據：[T07 紀錄](../../research/tutorial-audit/records/T07.md#t07-b)
- 上游 main `922563eab` 的實作仍相同：`ultralytics/utils/metrics.py` 的 `Metric.maps` 先用 `np.zeros(nc) + self.map` 填滿，再覆寫 `ap_class_index` 列出的類別。
- 程式內部沒有其他地方讀取 `maps`，所以這是說明問題，不建議改變回傳值。
- 2026-10-29 以 `box.maps`、`metrics.box.maps`、`ap_class_index maps` 搜尋議題與 PR，未找到同題討論。

## 最小修改範圍

只改 `docs/en/modes/val.md` 兩處程式註解（第 74 行與第 243 行附近），例如：

```python
metrics.box.maps  # mAP50-95 per class; classes absent from the val set hold the overall mAP
metrics.box.ap_class_index  # class indices that were actually evaluated
```

`tasks/detect.md`、`segment.md`、`pose.md`、`obb.md` 與 `guides/model-evaluation-insights.md` 有相同註解，共 9 處。先只改 `val.md`，維護者同意後再決定是否一併修改，避免一開始就擴大範圍。

## 送出前要做的事

1. 在官方最新 main 重新確認行號與實作。
2. 用 COCO8 重跑，確認 `len(ap_class_index) < nc` 時填值等於 `metrics.box.map`。
3. 依[第一章](../../research/contributing/docs/contribution-workflow.md)開乾淨分支與英文 PR。

## 不在範圍內

`SegmentMetrics.maps` 回傳 box 與 mask 兩組 mAP 的**相加值**。文件沒有示範讀取它，所以本提案不處理。

---

# T07 proposal: explain how `metrics.box.maps` fills classes that were not evaluated

Status: research draft, 2026-10-29. No branch, upstream change, or PR yet.

## Why

The docs describe `metrics.box.maps` as "a list containing mAP50-95 for each category". Classes absent from the validation set actually hold the **overall mAP**, not a per-class score. In a COCO8 run (T07), only 6 of 80 classes were evaluated; the other 74 entries all showed 0.695148, the overall mAP.

Readers who sort `maps` to find weak classes would treat filler values as measurements.

- Evidence: [T07 record](../../research/tutorial-audit/records/T07.md#t07-b)
- Upstream main `922563eab` is unchanged: `Metric.maps` in `ultralytics/utils/metrics.py` starts from `np.zeros(nc) + self.map` and overwrites only the classes in `ap_class_index`.
- No internal code reads `maps`, so this is a documentation issue; changing the return value is not proposed.
- Searches on 2026-10-29 for `box.maps`, `metrics.box.maps`, and `ap_class_index maps` found no matching issue or PR.

## Minimal change

Edit two code comments in `docs/en/modes/val.md` (around lines 74 and 243):

```python
metrics.box.maps  # mAP50-95 per class; classes absent from the val set hold the overall mAP
metrics.box.ap_class_index  # class indices that were actually evaluated
```

The same comment appears in 9 places across `tasks/` and `guides/`. Change `val.md` first and extend only if maintainers agree.

## Before submitting

1. Recheck line numbers and implementation on the latest upstream main.
2. Rerun COCO8 and confirm the filler equals `metrics.box.map` when `len(ap_class_index) < nc`.
3. Open a clean branch and an English PR following [chapter 1](../../research/contributing/docs/contribution-workflow.md).

## Out of scope

`SegmentMetrics.maps` returns the **sum** of box and mask mAPs. The docs do not show reading it, so this proposal leaves it alone.
