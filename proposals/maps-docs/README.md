# T07 提案：說明 `metrics.box.maps` 對未評估類別的填值

狀態：2026-10-30 已在最新 main `ae2857e3e`（8.4.193）以 COCO8 重新驗證：80 類只評估 6 類，其餘 74 格等於整體 mAP 0.669。已送出 [PR #26955](https://github.com/ultralytics/ultralytics/pull/26955)，分支 `docs/clarify-maps-filler`，第一個提交只改 `docs/en/modes/val.md` 兩處（+4/−2）。維護者 pderrenger 請我們把同樣的說明與 `ap_class_index` 那一行帶到其他頁面，追加提交 `d2fd73703` 已改完其餘 7 處，並在留言回覆。等待審查。PR 草稿與驗證見 [PR.md](PR.md)。

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

`tasks/detect.md`、`segment.md`、`pose.md`、`obb.md` 與 `guides/model-evaluation-insights.md` 有相同註解，共 7 處（連同 `val.md` 共 9 處）。先只改 `val.md`，維護者同意後再決定是否一併修改，避免一開始就擴大範圍。

**後續（2026-10-30）：** 維護者要求一併修改，追加提交 `d2fd73703` 改完這 7 處。任務頁依頁面上的 metric（`box`、`seg`、`pose`）各加一行 `ap_class_index`；評估指南原本就印出 `ap_class_index`，所以只加註解。驗證見 [verify_maps_all_tasks.log](assets/verify_maps_all_tasks.log)：COCO8 `box`、COCO8-seg 的 `box` 與 `seg` 都是 6 類評估、74 類填值，DOTA8 `box` 是 3 類評估、12 類填值。COCO8-pose 只有 1 類，看不到填值，但走同一段 `Metric.maps`。

## 送出前要做的事

1. 在官方最新 main 重新確認行號與實作。
2. 用 COCO8 重跑，確認 `len(ap_class_index) < nc` 時填值等於 `metrics.box.map`。
3. 依[第一章](../../research/contributing/docs/contribution-workflow.md)開乾淨分支與英文 PR。

## 不在範圍內

`SegmentMetrics.maps` 回傳 box 與 mask 兩組 mAP 的**相加值**。文件沒有示範讀取它，所以本提案不處理。

---

# T07 proposal: explain how `metrics.box.maps` fills classes that were not evaluated

Status: revalidated on latest main `ae2857e3e` (8.4.193) on 2026-10-30 with COCO8: 6 of 80 classes evaluated, the other 74 entries equal the overall mAP 0.669. Submitted as [PR #26955](https://github.com/ultralytics/ultralytics/pull/26955) on branch `docs/clarify-maps-filler`; the first commit changes two places in `docs/en/modes/val.md` (+4/−2). Maintainer pderrenger asked to carry the same note and `ap_class_index` line into the other pages. Follow-up commit `d2fd73703` covers the remaining 7 places, and a reply was posted. Awaiting review.

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

The same comment appears in 7 more places across `tasks/` and `guides/` (9 including `val.md`). Change `val.md` first and extend only if maintainers agree.

**Follow-up (2026-10-30):** maintainers asked for it, and commit `d2fd73703` updates those 7 places. Task pages get an `ap_class_index` line for each metric they show (`box`, `seg`, `pose`); the evaluation guide already prints `ap_class_index`, so it only gets the note. See [verify_maps_all_tasks.log](assets/verify_maps_all_tasks.log): COCO8 `box` and COCO8-seg `box`/`seg` each have 6 evaluated and 74 filler classes, and DOTA8 `box` has 3 and 12. COCO8-pose has one class, so there is no filler to observe; it uses the same `Metric.maps`.

## Before submitting

1. Recheck line numbers and implementation on the latest upstream main.
2. Rerun COCO8 and confirm the filler equals `metrics.box.map` when `len(ap_class_index) < nc`.
3. Open a clean branch and an English PR following [chapter 1](../../research/contributing/docs/contribution-workflow.md).

## Out of scope

`SegmentMetrics.maps` returns the **sum** of box and mask mAPs. The docs do not show reading it, so this proposal leaves it alone.
