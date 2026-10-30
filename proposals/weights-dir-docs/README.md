# T01／T05 提案：澄清 weights_dir 的查找與下載行為

狀態：2026-10-29 已在獨立功能 worktree 完成文件修改與本地驗證，已建立 [PR #26935](https://github.com/ultralytics/ultralytics/pull/26935)，2026-10-30（台灣時間）合併；維護者 Glenn Jocher 以 `e53a62c0f` 把 10 行說明段改寫為 `weights_dir` 表格列的說明，加上表格後一句註記，合併版本為 +3/−1。以下保留提案規劃；實際結果見 [PR 草稿的驗證段落](PR.md)。

實作位置：`D:/tools/ultralytics/.worktrees/weights-dir-docs`；分支：`docs/clarify-weights-dir`；基準：官方 main `922563eab`。最終只在 Settings Reference 前增加說明與範例，共 10 行，沒有修改表格或產品程式碼。驗證腳本位於本機 Temp 的 `verify_weights_dir_docs.py`，建置日誌為 `weights-dir-docs-build-final.log`。

目標是讓使用者讀完 Settings 頁，就能區分「查找既有權重」與「指定下載位置」。中英文提交草稿見 [PR 草稿](PR.md)，正式提交只使用英文。本頁英文版在下方。

## 為什麼值得做

T01 發現：設定 `weights_dir` 後，以裸模型檔名載入，缺少的權重仍下載到目前工作目錄。T05 的查找實測與原始碼核對進一步釐清：指定路徑已有檔案時先使用它，其次查找 `weights_dir`；缺檔下載不會一律改到該目錄。

官方 Settings 頁目前只把 `weights_dir` 描述為模型權重的儲存目錄，沒有交代這個差別。這是文件澄清候選，不是已確認需要改變下載邏輯的 bug。

- [T01 執行紀錄](../../research/tutorial-audit/records/T01.md)
- [T05 查找與設定驗證](../../research/tutorial-audit/records/T05.md)
- [目前 Settings 文件](https://github.com/ultralytics/ultralytics/blob/main/docs/en/usage/settings.md)
- [權重查找與下載實作](https://github.com/ultralytics/ultralytics/blob/main/ultralytics/utils/downloads.py)

## 舊議題關閉後，這個提案還有什麼用途

[#18435](https://github.com/ultralytics/ultralytics/issues/18435) 是使用方式提問，被標為 #17513 的重複議題。維護者說明查找用途並提供指定下載路徑的方法，提問者於 2024-12-31 自行關閉；不能把它描述為尚未修復的 bug。

文件提案的價值，是把[維護者已提供的解答](https://github.com/ultralytics/ultralytics/issues/18435#issuecomment-2565214274) 放到使用者會查閱的 Settings 頁。PR 使用 `Related to #18435 and #17513` 表達背景。

另有 [PR #24150](https://github.com/ultralytics/ultralytics/pull/24150) 嘗試改變裸檔名的下載位置，最後未合併。討論涉及 CI 與校正資料路徑，不能把其結果解讀成文件澄清已遭否決，也不宜直接重做同樣的行為變更。

## 最小修改範圍

實際只修改 `docs/en/usage/settings.md`，新增 10 行：

1. 在 Settings Reference 表格前說明：裸模型檔名先查目前工作目錄，再查 `weights_dir`；兩處皆無時下載到工作目錄。
2. 加入以 `Path(settings["weights_dir"]).resolve()` 明確指定下載路徑的範例。
3. 原表格保留；相鄰說明已足以釐清用途，無需另外修改表格。

說明必須限定已驗證的載入路徑；不可宣稱所有 URL、HUB、其他模型格式或下載 API 都遵循相同規則。先不改下載程式、不新增參數，也不把本地研究紀錄放進上游 PR。

## 提交前需完成的驗證

- [x] 查核當時最新 upstream main `922563eab42b778445e55a2edbabb6974eed8e4b` 的文件與程式碼；以 `repo:ultralytics/ultralytics is:pr is:open weights_dir` 搜尋得到 0 筆。這是關鍵字查重，不保證涵蓋不同措辭的 PR。
- [x] 已閱讀該版本的 `docs/AGENTS.md`，使用文件指定的 Prettier 版本與縮排。
- [x] 隔離目錄中的三種模型載入情境均通過：工作目錄優先、只有 `weights_dir` 有模型、兩處皆無時下載到工作目錄。
- [x] 明確指定下載路徑的範例通過實際下載及模型載入；已補齊 T05 未實測的情境。
- [x] 文件與實測一致；Prettier 3.9.9、`git diff --check`、UTF-8 模式下的 `python docs/build_docs.py` 完整嚴格建置通過。建置還原後確認只有 Settings 文件差異，暫存區為空。
- [x] 中英文 PR Validation 已填入基準版本、驗證情境與建置結果，移除未驗證占位文字。實際行為驗證命令為以既有 Python 環境執行 `%TEMP%/verify_weights_dir_docs.py`；完整腳本路徑與環境見下方。

T01／T05 舊證據使用 PyPI Ultralytics 8.4.191；本次新增驗證直接匯入功能 worktree 的原始碼，並檢查 `ultralytics.__file__`，不是沿用已安裝套件的結果。環境為 Windows／CPU、Python 3.13。沒有驗證其他作業系統、URL 或其他模型格式；若提交前基準或相關程式改變，再檢查受影響項目。

行為驗證的 PowerShell 命令（Temp 環境與腳本仍存在時可用）：

```powershell
& "$env:TEMP/ultralytics-tutorial-0d928fdb911d405f850a79ca00613d55/.venv/Scripts/python.exe" "$env:TEMP/verify_weights_dir_docs.py"
```

腳本會建立新的隔離目錄並下載公開模型。Temp 檔案可能遭清除，不能視為永久保存的驗證附件。

## 正式實作時

另從最新上游建立功能分支與 worktree，只帶入經驗證的文件修改。研究分支不拿來送上游 PR。這份草稿尚未取得維護者核可，也不代表保證會合併。

---

# English: T01/T05 proposal — clarify weights_dir lookup and downloads

Status: implemented and locally validated in a separate feature worktree on 2026-10-29. Submitted as [PR #26935](https://github.com/ultralytics/ultralytics/pull/26935), merged on 2026-10-30 (Taiwan time) as +3/−1: maintainer Glenn Jocher (`e53a62c0f`) folded the 10-line note into the `weights_dir` table row plus one sentence after the table. The proposal below is retained as planning context; see the [PR draft](PR.md) for actual validation results.

Worktree: `D:/tools/ultralytics/.worktrees/weights-dir-docs`; branch: `docs/clarify-weights-dir`; base: upstream main `922563eab`. The final change adds 10 lines of explanation and example before the settings table, without changing the table or product code. The local Temp directory contains `verify_weights_dir_docs.py` and the build log `weights-dir-docs-build-final.log`.

Help readers distinguish looking up existing weights from choosing a download location on the Settings page. See the bilingual [PR draft](PR.md); use only English for the upstream submission.

## Why this change is useful

T01 found that loading a bare model filename downloaded missing weights to the current working directory despite a configured `weights_dir`. T05 checked the lookup behavior and source: an existing file at the supplied path takes precedence, followed by a lookup under `weights_dir`. Missing files are not always downloaded into that directory.

The Settings page currently describes `weights_dir` as a model-weight storage directory without explaining this distinction. This is a documentation clarification candidate, not a confirmed need to change download behavior.

- [T01 execution record](../../research/tutorial-audit/records/T01.md)
- [T05 settings and lookup checks](../../research/tutorial-audit/records/T05.md)
- [Current Settings documentation](https://github.com/ultralytics/ultralytics/blob/main/docs/en/usage/settings.md)
- [Weight lookup and download implementation](https://github.com/ultralytics/ultralytics/blob/main/ultralytics/utils/downloads.py)

## Why this remains useful after the issues were closed

[#18435](https://github.com/ultralytics/ultralytics/issues/18435) was a usage question marked as a duplicate of #17513. A maintainer explained the lookup behavior and how to specify a download path. The author closed it on 2024-12-31. Do not describe it as an unresolved bug.

The proposal brings the [maintainer's existing answer](https://github.com/ultralytics/ultralytics/issues/18435#issuecomment-2565214274) into the Settings page. Use `Related to #18435 and #17513` in the PR to provide context.

[PR #24150](https://github.com/ultralytics/ultralytics/pull/24150) attempted to change bare-filename download locations but was not merged. Its discussion covered CI and calibration-data paths. That outcome does not establish that documentation clarification was rejected, nor justify repeating the behavior change.

## Smallest proposed change

The final change adds 10 lines only to `docs/en/usage/settings.md`:

1. Explain before the Settings Reference table that bare model filenames are looked up in the working directory, then `weights_dir`; missing weights download to the working directory.
2. Show an explicit download path using `Path(settings["weights_dir"]).resolve()`.
3. Keep the table unchanged: the adjacent explanation is sufficient to clarify its meaning.

Limit the explanation to the verified loading path. Do not claim that all URLs, HUB models, other formats, or download APIs follow the same rules. Keep download code, parameters, and local research records out of this upstream PR.

## Validation required before submission

- [x] Checked documentation and code at then-current upstream main `922563eab42b778445e55a2edbabb6974eed8e4b`. The query `repo:ultralytics/ultralytics is:pr is:open weights_dir` returned zero results; differently worded PRs may not appear.
- [x] Read that version's `docs/AGENTS.md` and used its prescribed Prettier version and indentation.
- [x] Verified working-directory precedence, weights_dir-only lookup, and download to the working directory when both locations lack the model.
- [x] Verified the explicit-path example with a real download and model load, covering the case T05 had not executed.
- [x] Confirmed the wording matches observed behavior. Prettier 3.9.9, `git diff --check`, and the full strict `python docs/build_docs.py` build in UTF-8 mode passed. After restoration, only the Settings page differs and the index is empty.
- [x] Updated both PR Validation versions with the source revision, scenarios, and build results, replacing placeholders. Behavior checks ran through `%TEMP%/verify_weights_dir_docs.py` using the existing Python environment; the command is below.

The earlier T01/T05 evidence used PyPI Ultralytics 8.4.191. The new checks imported source directly from the feature worktree and asserted its `ultralytics.__file__` path. They ran on Windows/CPU with Python 3.13. Other operating systems, URLs, and model formats were not tested. Recheck affected behavior if the base or relevant code changes before submission.

PowerShell command, while the Temp environment and script remain available:

```powershell
& "$env:TEMP/ultralytics-tutorial-0d928fdb911d405f850a79ca00613d55/.venv/Scripts/python.exe" "$env:TEMP/verify_weights_dir_docs.py"
```

The script creates a new isolated directory and downloads public weights. Temp files may be removed; they are not permanent validation attachments.

## Implementation workflow

Create a separate feature branch and worktree from the latest upstream revision. Include only the verified documentation change. Do not submit the research branch upstream. This draft has no maintainer approval and does not guarantee acceptance.
