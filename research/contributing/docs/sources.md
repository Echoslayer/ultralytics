# 來源、範圍與更新紀錄

## 研究快照

| 項目             | 本輪紀錄                                                               |
| ---------------- | ---------------------------------------------------------------------- |
| 查核日期         | 2026-10-28，工作環境時區 Asia/Taipei                                   |
| 本地基準         | `bb3e1550dbb819bd9846d4c99f368aebe8792a0e`                             |
| 基準 commit 日期 | 2026-10-27 22:47:32 UTC                                                |
| origin           | `https://github.com/Echoslayer/ultralytics.git`                        |
| 官方 main 查核   | `git ls-remote` 於本輪回傳同一 SHA；之後仍可能更新                     |
| 研究分支         | `research/contribution-book`，不開 PR                                  |
| 獨立 worktree    | `D:\tools\ultralytics\.worktrees\contribution-research`                |
| 正文位置         | `research/contributing/docs/`                                          |
| 參考出版方式     | `D:\vlm-jev\BOOKS.md`、`configs/community.yml`、`mkdocs-run.py` 與鎖檔 |

本書的 GitHub 固定 commit 連結使用 fork 地址，因為它是本地實際讀取的基準；即時 issue／PR 則連到官方 repo。不要將 fork 永久視為與 upstream 同步。

## 第一手來源索引

| 來源                                                                                                                                        | 用途與本輪閱讀範圍                                           |
| ------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| [CONTRIBUTING.md](https://github.com/ultralytics/ultralytics/blob/main/CONTRIBUTING.md)                                                     | 小型首次貢獻、功能事前討論、CLA、自動 review；與本地全文對照 |
| [官方貢獻指南](https://docs.ultralytics.com/help/contributing/)                                                                             | 貢獻種類與回報要求                                           |
| [官方 MRE 指南](https://docs.ultralytics.com/help/minimum-reproducible-example/)                                                            | 公開模型與輸入、環境、expected／actual                       |
| [AGENTS.md 固定快照](https://github.com/Echoslayer/ultralytics/blob/bb3e1550dbb819bd9846d4c99f368aebe8792a0e/AGENTS.md)                     | owner、最小 diff、worktree、測試與 review 工作流             |
| [docs/AGENTS.md 固定快照](https://github.com/Echoslayer/ultralytics/blob/bb3e1550dbb819bd9846d4c99f368aebe8792a0e/docs/AGENTS.md)           | 文件 owner、生成 reference 與官方文件建置                    |
| [issue 入口設定](https://github.com/Echoslayer/ultralytics/blob/bb3e1550dbb819bd9846d4c99f368aebe8792a0e/.github/ISSUE_TEMPLATE/config.yml) | 官方推薦的論壇、Discord 與 Reddit 管道；未讀取私人聊天內容   |
| [公開 issue 列表](https://github.com/ultralytics/ultralytics/issues)                                                                        | 尋找近期線索；未做完整議題統計                               |
| [公開論壇](https://community.ultralytics.com/)                                                                                              | 社群議題與支援案例；具體案例來源見案例章                     |
| [MkDocs configuration](https://www.mkdocs.org/user-guide/configuration/)                                                                    | 獨立 docs_dir、site_dir 與導覽設定                           |
| [Material 搜尋](https://squidfunk.github.io/mkdocs-material/setup/setting-up-site-search/)                                                  | 書籍搜尋配置                                                 |

七個案例的主文、關鍵留言、查核限制與直接連結統一放在 [Issue 與論壇案例](issues-and-community.md)，避免兩份清單日後更新不一致。

## 如何解讀本書的證據

**來源事實**表示網頁或固定程式快照可支持的敘述；它不代表本機已重現。**本書判斷**表示根據維護者回覆、驗證成本與既有實作做出的建議。**驗證門檻**是下一輪應完成的工作，不能列入已完成成果。

網頁擷取可能使用快取，正式選題前仍要重讀 issue 最後留言與現行 PR。研究不是 exhaustive triage：沒有列出所有 open issues、完整搜尋所有重複 PR，亦未查閱 Discord 或 Reddit 的討論內容。網路來源與本地基準時間不同時，以明確版本及留言日期保留差異。

## 出版與模型驗證分開

本輪可驗的是研究書能否嚴格建置、頁面與本地資源能否連結、搜尋索引是否產生。沒有執行 YOLO 訓練、推論、export、MPS／CUDA benchmark，也沒有確認候選 bug 可在本機重現。案例中的性能或修復敘述歸屬原作者，不能當成我們的量測結果。

未對外發文、認領 issue、簽署 CLA、推送研究分支或開 PR。原 checkout 的模型程式與官方文件不屬於這次修改範圍。

## 下一次更新

先更新基準 SHA 與日期，再查候選是否已有修復／PR。若被關閉，要記錄原因並調整行動路線，而不只改狀態欄。得到本地實驗後，把命令、環境和原始輸出放在研究記錄中，再將可支持的結論寫進正文。每次修改後執行 README 中的嚴格建置。
