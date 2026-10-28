# Ultralytics 開源貢獻研究書

這是個人研究資料，分支 `research/contribution-book` 不用於 PR。正文位於 `docs/`，沿用 `D:\vlm-jev` 的 MkDocs Material、uv script 與鎖檔方式。獨立放在 `research/contributing/`，避免混入官方 `docs/en/` 導覽與發布流程。

## 建置與閱讀

在這個資料夾開啟 PowerShell，執行：

```powershell
$env:UV_CACHE_DIR = Join-Path $PWD '.uv-cache'
uv run --locked mkdocs-run.py build --strict
uv run --locked mkdocs-run.py serve --dev-addr 127.0.0.1:8008
```

瀏覽 `http://127.0.0.1:8008/`，Ctrl+C 停止。首次執行需要下載出版依賴；不會安裝 Ultralytics 或模型訓練套件。依賴直接沿用參考專案的 `mkdocs-run.py.lock`，不修改根目錄 `pyproject.toml`。

建置結果為 `book/index.html`，可以直接開啟閱讀；完整搜尋請用 HTTP 預覽。分享靜態書時，複製整個 `book/`。產物與快取不納入 Git。中文介面與 jieba 斷詞沿用 Material 的搜尋支援，搜尋引擎設定 `lang: [en]`，並不表示正文必須用英文。

## 維護

更新章節時保留來源 URL、查核日期、事實與推論的區別。新增頁面同步更新 `mkdocs.yml` 的 nav，再執行嚴格建置。這本書沒有模型執行程式；案例是待重現的研究線索，不能把出版檢查當成 bug 已確認。

正式貢獻請另外從更新過的官方 upstream 建立乾淨分支／worktree，只帶入該題必要的修正；不要直接從研究分支開 PR。

## 本輪驗證（2026-10-28）

- `mkdocs build --strict` 通過。
- 7 個 HTML 檔案的本地連結、資源與錨點檢查通過。
- 搜尋索引產生 40 筆章節記錄，包含候選 issue 文字。
- 本機預覽使用 `http://127.0.0.1:8008/`；未做瀏覽器視覺與互動搜尋驗收。
- 首次建置時 jieba 在目前 Python 發出第三方 escape sequence 提示，不影響建置與索引產生。
