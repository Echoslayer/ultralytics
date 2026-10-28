# 來源與查核限制

**本書查過官方規範與七個公開案例，但尚未在本機重現模型問題。** 閱讀時請區分原作者的結果、本書的判斷，以及下一輪才要做的驗證。

## 研究使用哪個版本？

| 項目                         | 紀錄                                                                       |
| ---------------------------- | -------------------------------------------------------------------------- |
| 研究查核日期                 | 2026-10-28；工作環境時區為 Asia/Taipei                                     |
| 本地基準 SHA（Git 版本編號） | `bb3e1550dbb819bd9846d4c99f368aebe8792a0e`                                 |
| 基準提交時間                 | 2026-10-27 22:47:32 UTC                                                    |
| `origin` 遠端來源            | `https://github.com/Echoslayer/ultralytics.git`                            |
| 官方 `main` 查核             | 研究時用 `git ls-remote` 查到相同版本；之後仍可能更新                      |
| 研究分支                     | `research/contribution-book`，不用於提出合併請求                           |
| 獨立工作目錄                 | `D:\tools\ultralytics\.worktrees\contribution-research`                    |
| 正文位置                     | `research/contributing/docs/`                                              |
| 出版方式參考                 | `D:\vlm-jev\BOOKS.md`、`configs/community.yml`、`mkdocs-run.py` 與版本鎖檔 |
| 編寫標準                     | ISO 24495-1:2023 淺白語言原則；2026-10-28 依此改寫                         |

固定版本的程式連結指向個人副本，因為那是本地實際讀取的內容。議題與 PR（合併請求）則連到官方專案。個人副本不會永遠與官方同步。

## 官方文件與原始資料索引

| 來源                                                                                                                                      | 用來查證什麼？                                                         |
| ----------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| [CONTRIBUTING.md](https://github.com/ultralytics/ultralytics/blob/main/CONTRIBUTING.md)                                                   | 首次貢獻範圍、功能事前討論、貢獻者授權協議與自動審查；已與本地全文對照 |
| [官方貢獻指南](https://docs.ultralytics.com/help/contributing/)                                                                           | 貢獻種類與回報要求                                                     |
| [官方最小可重現範例指南](https://docs.ultralytics.com/help/minimum-reproducible-example/)                                                 | 公開模型與輸入、環境、預期與實際結果                                   |
| [AGENTS.md 固定版本](https://github.com/Echoslayer/ultralytics/blob/bb3e1550dbb819bd9846d4c99f368aebe8792a0e/AGENTS.md)                   | 負責模組、最小修改、獨立工作目錄、測試與審查流程                       |
| [docs/AGENTS.md 固定版本](https://github.com/Echoslayer/ultralytics/blob/bb3e1550dbb819bd9846d4c99f368aebe8792a0e/docs/AGENTS.md)         | 文件來源、自動生成參考頁與官方文件建置                                 |
| [議題入口設定](https://github.com/Echoslayer/ultralytics/blob/bb3e1550dbb819bd9846d4c99f368aebe8792a0e/.github/ISSUE_TEMPLATE/config.yml) | 官方推薦的論壇、Discord 與 Reddit 管道；未讀取私人聊天                 |
| [公開議題列表](https://github.com/ultralytics/ultralytics/issues)                                                                         | 近期問題線索；未統計全部議題                                           |
| [公開論壇](https://community.ultralytics.com/)                                                                                            | 使用者問題與支援案例；具體來源見案例章                                 |
| [MkDocs 設定文件](https://www.mkdocs.org/user-guide/configuration/)                                                                       | 正文目錄 `docs_dir`、產物目錄 `site_dir` 與導覽設定                    |
| [Material 搜尋文件](https://squidfunk.github.io/mkdocs-material/setup/setting-up-site-search/)                                            | 書籍搜尋設定                                                           |
| [ISO 24495-1:2023 標準介紹](https://www.iso.org/standard/78907.html)                                                                      | 淺白語言的編寫原則及適用範圍                                           |

七個案例的主文、關鍵留言、限制與直接連結放在[案例章](issues-and-community.md)。更新時只維護那份清單，避免同一案例出現不同版本。

## 哪些是事實，哪些是待驗證建議？

| 本書的標示             | 代表什麼？                                   | 不代表什麼？   |
| ---------------------- | -------------------------------------------- | -------------- |
| 來源說了什麼／本地確認 | 網頁或固定程式版本支持的敘述                 | 本機已重現問題 |
| 本書建議               | 根據維護者回覆、驗證成本與現有程式作出的判斷 | 官方已同意採納 |
| 下一步驗證             | 後續要執行的檢查                             | 已完成的成果   |

網頁可能使用快取。正式選題前，請再讀最新留言和正在審查的 PR。本書沒有列出所有未結議題，也沒有完整排除重複 PR；沒有閱讀 Discord 或 Reddit 討論內容。網頁與本地程式若來自不同時間，請以記錄的版本與留言日期區分。

## 出版通過，不表示模型問題已驗證

本輪出版檢查涵蓋嚴格建置、本地頁面與資源連結，以及搜尋索引。尚未執行以下工作：

- YOLO 訓練、推論或模型匯出。
- Apple MPS 或 NVIDIA CUDA 設備的效能測試。
- 在本機重現候選問題。

案例中的效能或修復結果屬於原作者，不能當成我們的測量結果。

本輪也沒有對外發文、認領議題、簽署貢獻者授權協議、推送研究分支或提出 PR。原工作目錄的模型程式與官方文件不在修改範圍內。

## 後續如何更新這本書？

1. 記錄新的基準版本與查核日期。
2. 檢查候選問題是否已修復，或已有同題 PR。
3. 如果議題關閉，記下原因並調整行動路線，不只修改狀態。
4. 如果完成本地實驗，保存命令、環境與原始輸出，再把證據支持的結論寫入正文。
5. 依 ISO 24495-1 的相關、找得到、看得懂、用得上四項原則檢查文字。
6. 執行書籍 README 中的嚴格建置。

這次改寫保留 2026-10-28 的研究內容，沒有重新查核所有議題狀態。編寫方法採用 `iso-24495` 技能的繁體中文手法；這是本書的編輯要求，不是 ISO 認證或標準全文符合性聲明。
