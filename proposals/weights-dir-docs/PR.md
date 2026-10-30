# PR 草稿：中英文版本 / Bilingual PR draft

中文供閱讀與討論，正式提交只複製英文標題與正文。2026-10-29 已在獨立 worktree 完成文件修改與本地驗證，已建立 [PR #26935](https://github.com/ultralytics/ultralytics/pull/26935)，2026-10-30（台灣時間）合併為 `5fc6050fd`；維護者合併前改寫了說明，最終 +3/−1。

## 中文閱讀版

### 建議標題

釐清 weights_dir 的模型查找與下載行為

### 建議正文

#### 摘要

釐清 `weights_dir` 如何影響模型查找，以及缺少的模型權重會下載到哪裡。

Settings 頁目前將它稱為儲存目錄，因此使用者可能以為 `YOLO("yolo26n.pt")` 會把缺少的權重下載到該處，但這個呼叫實際上會下載到目前工作目錄。

說明查找順序，並示範如何在載入模型時明確指定下載路徑。

相關議題：#18435、#17513。

#### 驗證

- 以官方 main `922563eab` 加上本次文件修改，在 Windows／Python 3.13 的隔離目錄驗證四種情境：工作目錄優先、只有 weights_dir 有模型、兩處皆無時下載到工作目錄，以及明確路徑下載。全部通過，包含兩次實際下載與模型載入。
- Prettier 3.9.9（tab-width 4、print-width 120）與 `git diff --check` 通過。
- 設定 `PYTHONUTF8=1` 後，`python docs/build_docs.py` 完整嚴格建置通過。首次執行遇到 Windows cp950 讀檔錯誤，重跑前清除建置留下的唯讀 clone。

---

## English submission draft

Status: implemented and locally validated on 2026-10-29 in a separate worktree. Submitted as [PR #26935](https://github.com/ultralytics/ultralytics/pull/26935) and merged on 2026-10-30 (Taiwan time) as `5fc6050fd`; the maintainer rewrote the note before merging (+3/−1).

## Suggested title

```text
Clarify weights_dir lookup and model download behavior
```

## Suggested body

```markdown
## Summary

Clarify how `weights_dir` affects model lookup and where missing model
weights are downloaded.

The Settings page currently calls it a storage directory. Users may
therefore expect `YOLO("yolo26n.pt")` to download missing weights there,
even though this call downloads them to the current working directory.

Explain the lookup order and show how to specify the download path when
loading a model.

Related to #18435 and #17513.

## Validation

- Checked upstream main `922563eab` with this documentation change on
  Windows/Python 3.13 in isolated directories. All four cases passed:
  working-directory precedence, weights_dir-only lookup, missing weights
  downloaded to the working directory, and an explicit download path.
  Checks included two real downloads and model loading.
- Prettier 3.9.9 (`--tab-width 4 --print-width 120`) and `git diff --check` passed.
- `python docs/build_docs.py` passed the full strict build with
  `PYTHONUTF8=1`. The first attempt hit a Windows cp950 decoding error;
  a leftover read-only build clone was removed before the successful rerun.
```

The section headings above are a suggested structure, not mandatory Ultralytics fields. Sources: [organization PR template](https://github.com/ultralytics/.github/blob/main/PULL_REQUEST_TEMPLATE.md) and [contribution guide](https://github.com/ultralytics/ultralytics/blob/main/CONTRIBUTING.md), checked on 2026-10-29.

上述章節是建議結構，不是 Ultralytics 必填欄位。依據為官方組織共用 PR 模板與貢獻指南，查核日期為 2026-10-29。
