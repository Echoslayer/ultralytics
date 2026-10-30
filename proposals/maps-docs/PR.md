# PR 草稿：中英文版本 / Bilingual PR draft

中文版供閱讀與討論；提交上游時只複製英文標題與正文。2026-10-30 已在獨立 worktree 完成修改與本地驗證，送出 [PR #26955](https://github.com/ultralytics/ultralytics/pull/26955)。

實作位置：`D:/tools/ultralytics/.worktrees/maps-docs`。分支：`docs/clarify-maps-filler`。基準：官方 main `ae2857e3e`（8.4.193）。只修改 `docs/en/modes/val.md` 兩處註解，+4/−2，沒有修改產品程式碼。驗證腳本與日誌見 [assets](assets/)。

這份草稿是在 PR 送出**之後**補寫的。送出時漏了本目錄的流程：沒有先寫 `PR.md`、沒跑文件建置，正文也沒寫未驗證範圍。之後已補跑檢查，2026-10-30 依英文版更新線上正文的 Summary 與 Validation，保留 bot 產生的 PR Summary。PR 當時已獲核可。

## 中文閱讀版

### 建議標題

說明 metrics.box.maps 對驗證集沒有的類別如何填值

### 建議正文

#### 摘要

文件說 `metrics.box.maps` 是每個類別的 mAP50-95。實際上，`Metric.maps` 會把驗證集裡沒出現的類別填成整體 mAP。用 `yolo26n.pt` 驗證 COCO8 時，80 個類別只評估了 6 個，其餘 74 格都等於 `metrics.box.map`（0.669）。讀者若排序 `maps` 找表現差的類別，會把填值當成實測。

這次修改在 `val.md` 的兩個範例中說明這件事，並加上 `ap_class_index`，列出真正評估過的類別。不修改程式碼。

`tasks/detect.md`、`segment.md`、`pose.md`、`obb.md` 與 `guides/model-evaluation-insights.md` 也有相同註解，需要的話可以一併修改。

#### 驗證

- 在官方 main `ae2857e3e` 上，以 Windows 11／CPU、Python 3.13.14、torch 2.15.0、numpy 2.5.4 跑 COCO8 驗證。assert 通過：未評估的 74 格等於 `box.map`，評估過的 6 格等於 `box.ap`。
- Prettier 3.9.9（`--tab-width 4 --print-width 120`）與 `git diff --check` 通過。
- `python docs/build_docs.py`：設定 `PYTHONUTF8=1` 後完整嚴格建置通過（No issues found，52 秒），建置後 docs 目錄已還原，工作樹乾淨。
- 沒有在 Linux 或 macOS 上測試。只驗證偵測任務的 `box.maps`；`seg`、`pose` 的 `maps` 用同一個 `Metric.maps`，但沒有實測。

---

## English submission draft

Status: implemented and locally validated on 2026-10-30 in a separate worktree. Submitted as [PR #26955](https://github.com/ultralytics/ultralytics/pull/26955). This draft was written after submission; the live body was updated with this Summary and Validation on 2026-10-30, keeping the bot-generated PR Summary. The PR was already approved at that point.

## Suggested title

```text
Explain how metrics.box.maps fills classes absent from the val set
```

## Suggested body

```markdown
## Summary

`metrics.box.maps` is documented as mAP50-95 for each category, but
`Metric.maps` fills classes that never appear in the validation set with
the overall mAP. On COCO8 with `yolo26n.pt`, only 6 of 80 classes are
evaluated; the other 74 entries equal `metrics.box.map` (0.669). Sorting
`maps` to find weak classes would treat these filler values as measurements.

This updates the two `val.md` examples to say so and shows
`ap_class_index`, which lists the classes that were actually evaluated.
No code changes.

The same comment appears in `tasks/detect.md`, `segment.md`, `pose.md`,
`obb.md`, and `guides/model-evaluation-insights.md`. Happy to update those
too if you'd like.

## Validation

- On main `ae2857e3e` (Windows 11, CPU, Python 3.13.14, torch 2.15.0,
  numpy 2.5.4), ran COCO8 val and asserted that the 74 non-evaluated
  entries equal `box.map` and the 6 evaluated entries equal `box.ap`.
- Prettier 3.9.9 (`--tab-width 4 --print-width 120`) and `git diff --check` passed.
- `python docs/build_docs.py`: passed the full strict build with `PYTHONUTF8=1` (no issues found).
- Not tested on Linux or macOS. Only detection `box.maps` was checked;
  `seg` and `pose` `maps` use the same `Metric.maps` but were not run.
```

The section headings above are a suggested structure, not mandatory Ultralytics fields.

上述章節是建議結構，不是 Ultralytics 必填欄位。
