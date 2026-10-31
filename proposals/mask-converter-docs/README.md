# T14 提案：修正 mask 轉換工具的輸入格式說明

狀態：2026-10-31 已在官方 main `58876de55`（8.4.194）完成修改與本地驗證。工作樹 `ultralytics/.worktree/mask-converter-docs`，分支 `docs/mask-converter-input`，commit `cdd83a3b6`，已送出 [PR #26971](https://github.com/ultralytics/ultralytics/pull/26971)，等待審查。只改 `docs/en/usage/simple-utilities.md` 一句（+1/−1），不改程式碼。PR 草稿見 [PR.md](PR.md)。

## 為什麼值得做

`simple-utilities.md` 說 `convert_segment_masks_to_yolo_seg` 吃「binary format」的 mask 圖片。實際上像素值要是類別索引 + 1，0 是背景。照「binary」準備最常見的 0/255 圖片，輸出的標籤檔是空的，只留一條 `Unknown class` 警告。

- 這句從 [#14557](https://github.com/ultralytics/ultralytics/pull/14557)（2024-08-01）留到現在。[#26370](https://github.com/ultralytics/ultralytics/pull/26370)（2026-09-27）已把 docstring 與 `datasets/segment/index.md` 改對，只漏了這一頁。
- [#15098](https://github.com/ultralytics/ultralytics/issues/15098) 的使用者就是用 0/255 的道路 mask 碰到這個問題。該 issue 已關閉，所以 PR 只引用，不寫 `Fixes`。
- 2026-10-31 用函式名稱和頁面名稱搜尋 open PR，沒有人在處理。
- 證據：[T14 紀錄](../../research/tutorial-audit/records/T14.md)

## 最小修改範圍

```markdown
This function takes the directory containing grayscale mask images, where each pixel value is the class index + 1 and 0 is background, and converts them into YOLO segmentation format.
```

措辭與 docstring 相同。

## 驗證

環境：macOS（Apple Silicon）、Python 3.13.12、torch 2.15.0、CPU。

- [`verify_mask_doc.py`](assets/verify_mask_doc.py) 寫出真的 PNG mask，對 worktree 的程式逐項檢查，全部符合（[`verify_mask_doc.log`](assets/verify_mask_doc.log)）：

| 像素值 | `classes` | 輸出類別 |
| --- | --- | --- |
| 1、2、3 | 80 | 0、1、2 |
| 只有背景 0 | 80 | 無 |
| 0、255 | 80 | 無，`Unknown class` 警告 |
| 0、1、255 | 80 | 0，255 被跳過並警告 |

- Prettier 3.9.9（`--tab-width 4 --print-width 120`）與 `git diff --check` 通過。
- `python docs/build_docs.py` 完整嚴格建置通過（No issues found，[`build-docs.log`](assets/build-docs.log)），工作樹只留這一處修改。
- 沒有在 Windows 或 Linux 上測試。

## 不在範圍內

- 讓工具接受 0/255 圖片，或把警告改得更明確：屬於程式行為變更，要另外討論。
- predict 來源表與 `batch` 說明（T14 候選 2）：主題無關，先留在 [T14](../../research/tutorial-audit/records/T14.md)。

---

# T14 proposal: correct the input format described for the mask converter

Status: implemented and locally validated on official main `58876de55` (8.4.194) on 2026-10-31. Worktree `ultralytics/.worktree/mask-converter-docs`, branch `docs/mask-converter-input`, commit `cdd83a3b6`, submitted as [PR #26971](https://github.com/ultralytics/ultralytics/pull/26971); awaiting review. Changes one sentence in `docs/en/usage/simple-utilities.md` (+1/−1), no code changes. PR draft: [PR.md](PR.md).

## Why

`simple-utilities.md` says `convert_segment_masks_to_yolo_seg` takes "binary format" mask images. In fact each pixel value must be the class index + 1, with 0 as background. A typical 0/255 image prepared as "binary" produces an empty label file and a single `Unknown class` warning.

- The sentence dates from [#14557](https://github.com/ultralytics/ultralytics/pull/14557) (2024-08-01). [#26370](https://github.com/ultralytics/ultralytics/pull/26370) (2026-09-27) corrected the docstring and `datasets/segment/index.md` but missed this page.
- The user in [#15098](https://github.com/ultralytics/ultralytics/issues/15098) hit this with a 0/255 road mask. That issue is closed, so the PR references it without `Fixes`.
- A search of open PRs by function name and page name on 2026-10-31 found none in progress.
- Evidence: [T14 record](../../research/tutorial-audit/records/T14.md)

## Minimal change

```markdown
This function takes the directory containing grayscale mask images, where each pixel value is the class index + 1 and 0 is background, and converts them into YOLO segmentation format.
```

The wording matches the docstring.

## Validation

Environment: macOS (Apple Silicon), Python 3.13.12, torch 2.15.0, CPU.

- [`verify_mask_doc.py`](assets/verify_mask_doc.py) writes real PNG masks and checks the worktree's code; every case matches ([`verify_mask_doc.log`](assets/verify_mask_doc.log)):

| Pixel values | `classes` | Output classes |
| --- | --- | --- |
| 1, 2, 3 | 80 | 0, 1, 2 |
| Background 0 only | 80 | None |
| 0, 255 | 80 | None, `Unknown class` warning |
| 0, 1, 255 | 80 | 0; 255 skipped with a warning |

- Prettier 3.9.9 (`--tab-width 4 --print-width 120`) and `git diff --check` pass.
- `python docs/build_docs.py`: full strict build passed (no issues found, [`build-docs.log`](assets/build-docs.log)); only this change remains in the working tree.
- Not tested on Windows or Linux.

## Out of scope

- Accepting 0/255 images or rewording the warning: a code behavior change that needs separate discussion.
- The predict source table and `batch` description (T14 candidate 2): unrelated topic, kept in the [T14 record](../../research/tutorial-audit/records/T14.md).

這些是研究草稿，不代表已取得維護者同意。/ This is a research draft, not evidence of maintainer approval.
