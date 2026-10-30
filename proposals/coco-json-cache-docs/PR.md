# PR 草稿：中英文版本 / Bilingual PR draft

中文版供閱讀與討論；提交上游時只複製英文標題與正文。2026-10-30 已在獨立 worktree 完成修改與本地驗證，**尚未送出**。

實作位置：`D:/tools/ultralytics/.worktrees/coco-json-cache`。分支：`docs/coco-json-cache-mtime`（已推到 Echoslayer fork）。基準：官方 main `ae2857e3e`（8.4.193）。commit `3003c19e3`、`df0fa429b`，只修改 `docs/en/guides/coco-json-training.md` 兩處，+3/−3，沒有修改產品程式碼。驗證腳本與日誌見 [assets](assets/)。

## 中文閱讀版

### 建議標題

依含修改時間的雜湊，更新 COCO JSON 指南的快取說明

### 建議正文

#### 摘要

`guides/coco-json-training.md` 的快取警告說，`get_hash()` 只看檔案大小，所以長度不變的 JSON 修改會沿用舊快取。#26283 把每個路徑的修改時間加進雜湊後，這已不成立。這段警告是一個月前（#25919）寫的，沒有跟著更新。

在 main 上，把框寬從 `611.59` 改成 `211.59`（JSON 大小不變），下次載入就會重新解析並讀到新值。只有把原本的修改時間還原，才會沿用舊快取。

這次把警告改寫成 note，並更新 FAQ 中對應的一句。檢查時另外發現一種仍會靜默沿用舊快取的情況，新的 note 也寫進去了：圖片放在子資料夾。`get_hash()` 只看 `img_path` 這個資料夾本身，所以 `file_name` 像 `sub/img.jpg` 時，把原本缺的圖片補進 `sub/` 不會改變雜湊。在刪除 `.cache` 之前，那張圖片會一直被排除，而且沒有任何訊息：`cache_labels()` 會跳過不存在的檔案，命中快取時也不印紀錄。不修改程式碼。

#### 驗證

- 在 main `ae2857e3e`（Windows 11、CPU、Python 3.13.14、torch 2.15.0）上，把 COCO8 轉成 COCO JSON，跑指南的 Full Implementation 1 個 epoch；再原樣使用指南的 `COCODataset` 測以下情況：

  | 修改 | 快取 |
  | --- | --- |
  | 不修改 | 命中 |
  | JSON 長度不變的修改 | 重新解析 |
  | 修改 JSON 後還原修改時間 | 命中（舊快取） |
  | 直接在 `img_path` 底下新增／刪除圖片 | 重新解析 |
  | 原地替換圖片 | 命中 |
  | 在子資料夾新增／刪除圖片 | 命中（舊快取） |

- Linux（WSL2 Ubuntu、ext4）：用從 `ultralytics/data/utils.py` 原樣取出的 `get_hash()` 檢查相同情況；快取只在雜湊不變時命中。全部符合。步驟間不暫停時，在同一個 4 ms 時間戳刻度內新增再刪除檔案，資料夾大小與修改時間都不變；實際修改相隔數秒，不會發生。
- Prettier 3.9.9（`--tab-width 4 --print-width 120`）與 `git diff --check` 通過。
- `python docs/build_docs.py`：設定 `PYTHONUTF8=1` 後完整嚴格建置通過（no issues found）。
- 沒有在 macOS 上測試。

---

## English submission draft

Status: implemented and locally validated on 2026-10-30 in a separate worktree. **Not yet submitted.**

## Suggested title

```text
Update the COCO JSON guide's cache note for mtime-aware hashing
```

## Suggested body

```markdown
## Summary

The cache warning in `guides/coco-json-training.md` says `get_hash()` keys on file size only, so a same-length JSON edit keeps the stale cache. That stopped being true in #26283, which added each path's modification time to the hash. The warning was written a month earlier (#25919) and was not updated.

On main, changing a box width from `611.59` to `211.59` (JSON size unchanged) re-parses the JSON on the next load and picks up the new value. The stale cache only survives if the original modification time is restored.

This rewrites the warning as a note and updates the matching FAQ sentence. While checking it, I found one case where the cache still goes stale silently, which the note now covers: images in a subfolder. `get_hash()` stats the `img_path` folder itself, so with a `file_name` like `sub/img.jpg`, adding a previously missing image to `sub/` does not change the key. The image stays excluded until `.cache` is deleted, with no message, since `cache_labels()` skips missing files and a cache hit logs nothing. No code changes.

## Validation

- On main `ae2857e3e` (Windows 11, CPU, Python 3.13.14, torch 2.15.0), ran the guide's Full Implementation on COCO8 converted to COCO JSON for 1 epoch, then the cases below with the guide's `COCODataset` used verbatim:

  | Change | Cache |
  | --- | --- |
  | none | hit |
  | same-size JSON edit | re-parse |
  | JSON edit with original mtime restored | hit (stale) |
  | add / remove an image directly in `img_path` | re-parse |
  | replace an image in place | hit |
  | add / remove an image in a subfolder | hit (stale) |

- Linux (WSL2 Ubuntu, ext4): checked the same cases against `get_hash()` taken verbatim from `ultralytics/data/utils.py`, since the cache hits exactly when that hash is unchanged. All match. Without a pause between steps, adding then removing a file within one 4 ms timestamp tick leaves the folder's size and mtime unchanged; with real edits seconds apart this does not occur.
- Prettier 3.9.9 (`--tab-width 4 --print-width 120`) and `git diff --check` passed.
- `python docs/build_docs.py`: passed the full strict build with `PYTHONUTF8=1` (no issues found).
- Not tested on macOS.
```

The section headings above are a suggested structure, not mandatory Ultralytics fields.

上述章節是建議結構，不是 Ultralytics 必填欄位。
