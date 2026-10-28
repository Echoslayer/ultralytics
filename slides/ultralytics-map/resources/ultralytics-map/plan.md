# Ultralytics repo 與測試需求地圖

## 目的與範圍

- 熟悉 Python 的貢獻者要判斷哪些檔案好改、哪些難改，以及實際缺多少測試證據。
- 對照 PySpark AgentDeck：保留目錄下鑽、卡片展開、函式起點與下一站；新增獨立的修改／補測試難度、逐檔覆蓋率、未覆蓋符號與輸入／assertion。
- 231 個套件 Python 檔全部索引；85 檔實讀（utils 22、integrations 8、engine/data/cfg/trackers 25、models/nn/optim/solutions 30）。其餘146檔不推定難度。
- 52個目錄節點保留原有層級；終端目錄收納更深的重要檔案，測試頁可搜尋所有Python檔。
- Python 原碼、tests、人工 edits、框架核心與其他研究資料唯讀；不提交、不發布、不跑模型、不新增依賴。

## 來源與資料契約

- 本機 HEAD：308ebb92e153bb0f711e46309a5b570f70a66f78；既有 research/contributing/docs/contribution-workflow.md 修改不屬本次。
- Codecov head：bb3e1550dbb819bd9846d4c99f368aebe8792a0e，查核2026-10-28。
- API：https://api.codecov.io/api/v2/github/ultralytics/repos/ultralytics/report/?sha=bb3e1550dbb819bd9846d4c99f368aebe8792a0e
- 保存原始報告 codecov-snapshot.json 作為正式證據附件；216檔、30,746行、19,429 hits、11,317 misses；逐行狀態0=hit、1=miss，已以totals交叉核對。
- 216個報告檔與本機工作檔逐檔內容一致（CRLF/LF正規化）；不是本機跑測試所得。
- 15個未收錄檔不當成0%；callbacks被pyproject明確omit，另外部分為空初始化檔。百分比使用API回傳值（部分小數截位），不是自行重估。
- Python標準庫AST定位最內層函式／類別，decorators納入歸屬；漏行區段不表示branch coverage。
- audit-*.json 是正式逐檔調查資料；coverage-crosscheck.json記錄10檔的16個漏行候選與8項修正。已覆蓋案例改標既有回歸，不冒充新缺口。
- test-map-data.js由上述資料生成；來源可離線讀取，GitHub/Codecov外連固定報告commit。

## 分工與判斷

- 依使用者要求，3位GPT-6.1 Sol分多輪調查、擴充整合邊界、交叉審查資料與UI；未用Astra。
- 主代理負責Codecov、逐檔版本校對、AST對照、共同UI與驗收。
- 修改難度以共享責任、數值語義、相容性與影響面判斷；測試難度以可控輸入、可斷言結果、狀態、硬體與服務依賴判斷。每檔理由優先於三級標籤。
- Codecov 0%不是無測試的證明。Triton有真HTTP smoke；TensorBoard integration可能被TESTS_RUNNING guard停用；RKNN產物測試不等於實機runtime通過。

## 分鏡與互動

1. 封面：先問改得動、驗得了。
2. Repo能力：任務與模式，cards並列。
3. 責任架構：入口／流程／資料與執行，cards並列。
4. 使用需求：保留8條需求路線。
5. 深度測試地圖：搜尋路徑／符號，模組、修改難度、測試難度、覆蓋率與深讀範圍篩選；排序、詳情、具體漏行與原碼。
6. 目錄卡片：展開不切目錄，保持fileOpen；下一站跳到指定測試檔案。
7. Codecov：模組分布、CI環境與快照限制。
8. 貢獻：可重現證據、最小修正、真實環境驗證。
9. 結尾：回到需求選題。

互動延伸既有主題原生控制項，不加依賴；mount有清理函式，previewArt有代表性靜態摘要。保留edits.js。

## 重建與自檢

從repo根目錄用已安裝Python執行 slides/ultralytics-map-research/build.py，再 node slides/ultralytics-map-research/check.cjs。
生成工具在簡報外；資料和逐檔調查屬正式內容，不是暫存測試報告。

## 驗收

- JS語法、所有231張卡片渲染、85筆中文、來源符號／測試函式、216檔逐行加總與版本一致性自檢。
- Chrome HTTP：搜尋activation、容易+漏行篩選、函式漏行展開、空結果、清除、全部檔案未收錄15筆、目錄下鑽及Results下一站。
- 窄螢幕DOM檢查：實際583px viewport未見橫向溢出；截圖API逾時，已還原viewport。桌面截圖已目視。
- 原始file://直開未驗證；外部權重／GPU／實際測試提案未執行。
- 最後pack與解壓版本驗證結果在交付時追加。

- 最終：231張卡片、85筆評估、16候選與9頁自檢通過；CLI pack成功。解壓副本用本機HTTP驗證搜尋、困難+低覆蓋篩選、排序、焦點保留與漏行提案，console無錯誤。仍未直接以file://實播。
