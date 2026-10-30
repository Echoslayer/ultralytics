# PR 草稿：中英文版本 / Bilingual PR draft

中文版供閱讀與討論；提交上游時只複製英文標題與正文。2026-10-30 已在獨立 worktree 完成修改與本地驗證，送出 [PR #26960](https://github.com/ultralytics/ultralytics/pull/26960)。

實作位置：`D:/tools/ultralytics/.worktrees/coco-json-cache`。分支：`docs/coco-json-cache-mtime`（已推到 Echoslayer fork）。基準：官方 main `ae2857e3e`（8.4.193）。commit `3003c19e3`、`df0fa429b`，只修改 `docs/en/guides/coco-json-training.md` 兩處，+3/−3，沒有修改產品程式碼。驗證腳本與日誌見 [assets](assets/)。

## 中文閱讀版

### 建議標題

雜湊已含修改時間，更新 COCO JSON 指南的快取說明

### 建議正文

#### 摘要

COCO JSON 指南警告：標註快取只看 JSON 的檔案大小，所以位元組數不變的修改，會在不知不覺中用舊標註訓練。寫這段警告時（#25919）確實如此，但後來 #26283 把修改時間加進了 `get_hash()`，現在編輯 JSON 就會照預期重新解析。我在 main 上試過：把一個框寬從 `611.59` 改成 `211.59`，檔案大小完全一樣，下次載入就讀到了新值。

所以這段警告現在多半是在叫大家刪一個不必刪的快取。我把它改成一段簡短的 note，並修正 FAQ 裡對應的那句。

測試時我確實碰到一種情況，快取仍會在毫無跡象下過時：圖片放在子資料夾裡。雜湊只看 `img_path` 這個資料夾本身，所以如果 `file_name` 是 `sub/img.jpg` 這類路徑，事後把缺的圖片補進 `sub/`，什麼都不會變，那張圖片會一直被排除在訓練外，直到刪掉 `.cache`。note 裡寫了這點，讓大家知道什麼時候仍需要手動刪除。

只改文件，不改程式碼。

#### 驗證

- 把 COCO8 轉成 COCO JSON，跑指南的 Full Implementation 一個 epoch（main `ae2857e3e`、Windows 11、CPU、Python 3.13.14、torch 2.15.0），再用指南原樣的 `COCODataset` 逐句檢查新 note：編輯 JSON 會重新解析；還原修改時間會留下舊快取；在最上層新增或刪除圖片會重建；原地替換和子資料夾裡的變動不會。
- 在 Linux（WSL2、ext4）上直接對 `get_hash()` 做同樣的檢查，因為快取命中與否就由它決定。結果相同。（有個小插曲：在同一個約 4 ms 的時間戳刻度內新增再刪除檔案，資料夾看起來會沒變，但實際修改不會碰到。）
- Prettier 3.9.9 與 `git diff --check` 通過，`python docs/build_docs.py` 建置沒有問題。
- 還沒在 macOS 上試過。

---

## English submission draft

Status: implemented and locally validated on 2026-10-30 in a separate worktree. Submitted as [PR #26960](https://github.com/ultralytics/ultralytics/pull/26960).

## Suggested title

```text
Update the COCO JSON guide's cache note now that the hash includes mtime
```

## Suggested body

```markdown
## Summary

The COCO JSON guide warns that the label cache only looks at the JSON's file size, so an edit that keeps the same byte count would silently train on old annotations. That was true when the warning was written (#25919), but #26283 later added modification times to `get_hash()`, so editing the JSON now re-parses it as you'd expect. I tried it on main: changing a box width from `611.59` to `211.59` keeps the file size identical, and the next load picked up the new value.

So the warning is now mostly telling people to delete a cache they don't need to delete. I've turned it into a short note and fixed the matching FAQ line.

While testing I did hit one case where the cache still goes stale without any sign: images in a subfolder. The hash only looks at the `img_path` folder itself, so if `file_name` is something like `sub/img.jpg` and you add a missing image to `sub/` later, nothing changes and that image just stays out of training until you delete the `.cache`. The note mentions this so people know when a manual delete is still needed.

Docs only, no code changes.

## Validation

- Ran the guide's Full Implementation for one epoch on COCO8 converted to COCO JSON (main `ae2857e3e`, Windows 11, CPU, Python 3.13.14, torch 2.15.0), then checked each sentence of the new note using the guide's `COCODataset` as written: JSON edits re-parse, a restored mtime keeps the old cache, top-level image adds and removes rebuild, and in-place replacements and subfolder changes don't.
- Repeated the same checks on Linux (WSL2, ext4) against `get_hash()` directly, since that's what decides a cache hit. Same results. (One quirk: if you add and remove a file within the same ~4 ms timestamp tick, the folder looks unchanged, but real edits don't run into that.)
- Prettier 3.9.9 and `git diff --check` pass, and `python docs/build_docs.py` builds cleanly.
- I haven't tried macOS.
```

The section headings above are a suggested structure, not mandatory Ultralytics fields.

上述章節是建議結構，不是 Ultralytics 必填欄位。
