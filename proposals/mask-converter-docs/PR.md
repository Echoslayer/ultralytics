# PR 草稿：中英文版本 / Bilingual PR draft

中文版供閱讀與討論；提交上游時只複製英文標題與正文。2026-10-31 已在獨立 worktree 完成修改與本地驗證，送出 [PR #26971](https://github.com/ultralytics/ultralytics/pull/26971)。

實作位置：`ultralytics/.worktree/mask-converter-docs`。分支：`docs/mask-converter-input`（已推到 Echoslayer fork）。基準：官方 main `58876de55`（8.4.194）。commit `cdd83a3b6`，只修改 `docs/en/usage/simple-utilities.md` 一句，+1/−1，沒有修改產品程式碼。驗證腳本與日誌見 [assets](assets/)。

## 中文閱讀版

### 建議標題

修正 Simple Utilities 頁對 mask 轉換工具輸入格式的說明

### 建議正文

#### 摘要

Simple Utilities 頁說 `convert_segment_masks_to_yolo_seg` 吃「binary format」的 mask 圖片，但它其實要求每個像素值是類別索引 + 1，0 是背景。照字面準備常見的 0/255 mask，會得到空的標籤檔，只有一條 `Unknown class` 警告。#15098 的使用者就碰過這個問題。

#26370 已經把 docstring 和 `datasets/segment/index.md` 改對了，這頁是唯一還留著舊說法的地方，所以我直接沿用 docstring 的措辭。

只改文件，不改程式碼。

#### 驗證

- 在 main `58876de55`（macOS、CPU、Python 3.13.12、torch 2.15.0）用真的 PNG mask 跑轉換：像素值 1、2、3 輸出類別 0、1、2；只含 0 和 255 時輸出空檔案並警告；1 和 255 混在一起時只留下類別 0。
- Prettier 3.9.9 與 `git diff --check` 通過，`python docs/build_docs.py` 建置沒有問題。
- 還沒在 Windows 或 Linux 上試過。

---

## English submission draft

Status: implemented and locally validated on 2026-10-31 in a separate worktree. Submitted as [PR #26971](https://github.com/ultralytics/ultralytics/pull/26971).

## Suggested title

```text
Correct the mask format described for convert_segment_masks_to_yolo_seg
```

## Suggested body

```markdown
## Summary

The Simple Utilities page says `convert_segment_masks_to_yolo_seg` takes "binary format" mask images, but it actually expects each pixel value to be the class index + 1, with 0 as background. A typical 0/255 mask prepared from that description gives an empty label file and one `Unknown class` warning, which is what the user in #15098 ran into.

#26370 already corrected the docstring and `datasets/segment/index.md`. This page is the one place still using the old description, so I reused the docstring's wording.

Docs only, no code changes.

## Validation

- Ran the converter on real PNG masks on main `58876de55` (macOS, CPU, Python 3.13.12, torch 2.15.0): pixel values 1, 2, 3 give classes 0, 1, 2; a mask with only 0 and 255 gives an empty file and a warning; 1 mixed with 255 keeps only class 0.
- Prettier 3.9.9 and `git diff --check` pass, and `python docs/build_docs.py` builds cleanly.
- I haven't tried Windows or Linux.
```

The section headings above are a suggested structure, not mandatory Ultralytics fields.

上述章節是建議結構，不是 Ultralytics 必填欄位。
