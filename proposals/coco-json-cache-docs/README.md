# T13 提案：更新 COCO JSON 指南的快取說明

狀態：2026-10-30 已在官方 main `ae2857e3e`（8.4.193）完成修改與本地驗證。分支 `docs/coco-json-cache-mtime`，已送出 [PR #26960](https://github.com/ultralytics/ultralytics/pull/26960)，等待審查。只改 `docs/en/guides/coco-json-training.md` 兩處（+3/−3），不改程式碼。PR 草稿見 [PR.md](PR.md)。

## 為什麼值得做

指南的警告說，快取只看 JSON 的檔案大小：修改後若位元組數不變，就會沿用舊快取、用舊標註訓練，而且沒有任何警告。這在 [#26283](https://github.com/ultralytics/ultralytics/pull/26283)（2026-09-23）之後已不成立，因為 `get_hash()` 改成同時看每個路徑的大小與修改時間。警告是 [#25919](https://github.com/ultralytics/ultralytics/pull/25919)（2026-08-25）寫的，比程式修改早一個月，之後沒有更新。

讀者照舊警告操作不會出錯，只是多刪快取。真正的問題是警告沒提到的情況：**圖片放在子資料夾裡**（`file_name` 像 `sub/img.jpg`）。雜湊只看 `img_path` 這個最上層資料夾，把缺的圖片補進子資料夾後，快取不會失效，那張圖片會一直被排除在訓練外。`cache_labels()` 找不到圖片時直接跳過，命中快取時也不印任何訊息，所以使用者不會察覺。

- 證據：[T13 紀錄](../../research/tutorial-audit/records/T13.md)
- 實測：寬度 611.59 改成 211.59，JSON 大小不變，下次載入就重新解析並讀到新值；只有手動還原修改時間，才會沿用舊快取。
- 子資料夾：JSON 列 4 張圖、只放 3 張；補進第 4 張再跑仍只用 3 張，刪掉 `.cache` 後才是 4 張（[`probe_t13d.py`](assets/probe_t13d.py)、[`t13d.log`](assets/t13d.log)）。
- #26283 只改了 `ultralytics/data/utils.py`，沒動文件。`docs/en/` 只有這頁提到快取鍵只看大小。2026-10-30 搜尋 `coco-json-training` 與快取相關的 PR，沒有人在處理。

## 最小修改範圍

1. 把 `!!! warning` 改成 `!!! note`，內容改成：快取鍵是每個路徑的大小與修改時間，編輯 JSON 會自動重新解析；圖片目錄只算最上層資料夾，直接在底下新增或刪除會重建，原地替換或在子資料夾裡增刪不會；這些情況，以及工具改寫 JSON 後還原修改時間時，要手動刪 `.cache`。
2. FAQ 最後一句改成「快取以 JSON 的大小與修改時間為鍵，編輯後會自動重新解析」。

## 驗證

- **Windows 11（NTFS）：** [`verify_note.py`](assets/verify_note.py) 直接取用修正分支文件裡的 `COCODataset`，用自產圖片逐句測新 note，10 項全部符合（[`verify_win.log`](assets/verify_win.log)）。
- **Linux（WSL2 Ubuntu、ext4）：** WSL 沒有 torch，改用 [`verify_hash_posix.py`](assets/verify_hash_posix.py) 從原始碼原樣抽出 `get_hash` 執行；快取命中與否只由這個雜湊決定。步驟間隔 50 ms 時 8 項全部符合（[`verify_linux.log`](assets/verify_linux.log)）。沒有間隔時，「在最上層刪除圖片」雜湊不變：ext4 刪檔後資料夾大小維持 4096，時間戳每 4 ms 才跳一格。實際增刪至少隔數秒，不影響 note 的說法。
- Prettier 3.9.9（`--tab-width 4 --print-width 120`）檢查 commit 內容通過；`git diff --check` 通過。工作目錄副本因 CRLF 換行會出現警告，commit 是 LF。
- `python docs/build_docs.py`：設定 `PYTHONUTF8=1` 後完整嚴格建置通過（No issues found，約 42 秒，[`build-docs.log`](assets/build-docs.log)），工作樹乾淨。
- 沒有在 macOS 上測試。

## 不在範圍內

- 指南的 `COCODataset` 程式碼本身：子資料夾的問題可以改用逐檔雜湊解決，但會讓範例變長，也偏離 `GroundingDataset` 的做法。先只修說明，維護者想要再改程式碼。
- 時間戳精度粗的檔案系統（例如 FAT32 的 2 秒）：理論上可能讓修改時間相同，沒有實測，不寫進文件。

---

# T13 proposal: update the COCO JSON guide's cache note

Status: implemented and locally validated on official main `ae2857e3e` (8.4.193) on 2026-10-30. Branch `docs/coco-json-cache-mtime`, submitted as [PR #26960](https://github.com/ultralytics/ultralytics/pull/26960); awaiting review. Changes two places in `docs/en/guides/coco-json-training.md` (+3/−3), no code changes. PR draft: [PR.md](PR.md).

## Why

The guide warns that the cache keys on the JSON's file size only, so a same-length edit keeps the stale cache and trains on old annotations with no warning. That stopped being true in [#26283](https://github.com/ultralytics/ultralytics/pull/26283) (2026-09-23), which hashes each path's size and modification time. The warning came from [#25919](https://github.com/ultralytics/ultralytics/pull/25919) (2026-08-25), a month earlier, and was not updated.

Following the old warning does no harm beyond extra cache deletions. The real gap is a case it does not mention: **images in a subfolder** (a `file_name` like `sub/img.jpg`). The hash only stats the top-level `img_path` folder, so adding a missing image to the subfolder does not invalidate the cache, and that image stays out of training. `cache_labels()` skips missing images silently and a cache hit logs nothing, so users would not notice.

- Evidence: [T13 record](../../research/tutorial-audit/records/T13.md)
- Measured: changing a width from 611.59 to 211.59 (same JSON size) re-parses on the next load and picks up the new value; the stale cache survives only if the modification time is restored by hand.
- Subfolder: the JSON lists 4 images with 3 present; adding the 4th still uses 3, and deleting `.cache` gives 4 ([`probe_t13d.py`](assets/probe_t13d.py), [`t13d.log`](assets/t13d.log)).
- #26283 changed only `ultralytics/data/utils.py`. No other page in `docs/en/` makes the size-only claim. A search on 2026-10-30 for PRs on `coco-json-training` and the cache found none in progress.

## Minimal change

1. Change `!!! warning` to `!!! note`: the key is each path's size and modification time, so editing the JSON re-parses it; the image directory counts only as a folder, so adding or removing an image directly inside it rebuilds, but replacing one in place or changing a subfolder does not; delete `.cache` in those cases, or if a tool rewrites the JSON and restores its modification time.
2. Change the last FAQ sentence to say the cache is keyed on the JSON's size and modification time, so edits re-parse automatically.

## Validation

- **Windows 11 (NTFS):** [`verify_note.py`](assets/verify_note.py) uses the `COCODataset` from the fix branch's guide verbatim with generated images and checks each sentence of the new note; all 10 cases match ([`verify_win.log`](assets/verify_win.log)).
- **Linux (WSL2 Ubuntu, ext4):** WSL has no torch, so [`verify_hash_posix.py`](assets/verify_hash_posix.py) runs `get_hash` taken verbatim from the source; the cache hits exactly when that hash is unchanged. With 50 ms between steps all 8 cases match ([`verify_linux.log`](assets/verify_linux.log)). Without a pause, removing a top-level image leaves the hash unchanged: ext4 keeps the folder size at 4096 after unlink and timestamps tick every 4 ms. Real edits seconds apart are unaffected.
- Prettier 3.9.9 (`--tab-width 4 --print-width 120`) passed on the committed content; `git diff --check` passed. The working-copy file shows a warning only because of CRLF line endings; the commit uses LF.
- `python docs/build_docs.py`: full strict build passed with `PYTHONUTF8=1` (no issues found, about 42 s, [`build-docs.log`](assets/build-docs.log)); working tree clean.
- Not tested on macOS.

## Out of scope

- The guide's `COCODataset` code itself: per-file hashing would fix the subfolder case but lengthen the example and diverge from `GroundingDataset`. Docs first; code only if maintainers want it.
- Filesystems with coarse timestamps (for example FAT32's 2 s): could in theory keep the same modification time, but untested and not documented.

這些是研究草稿，不代表已取得維護者同意。/ This is a research draft, not evidence of maintainer approval.
