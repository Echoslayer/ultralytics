# 3. 七個案例：哪些值得查，哪些先不要改

**先讀最新討論，再決定是否動手。** 議題仍開啟，不表示問題還沒解決；標為錯誤，也不表示根因在 Ultralytics。

以下資料查核於 **2026-10-28**，來自官方 GitHub 與論壇。這不是完整待辦清單，也沒有認領任何工作。網頁可能有數日快取；Open 代表頁面顯示仍開啟，Merged 代表已合併。正式選題前，請重新查看最後留言與相關 PR（合併請求）。

本章的「本書建議」與「下一步驗證」都是研究判斷；本輪沒有重跑模型實驗。

## 按你需要的證據選討論管道

官方分別提供文件、論壇、Discord 聊天社群與 GitHub 回報管道。本書建議先釐清使用方式，再把可獨立重現的套件問題整理到 GitHub，避免把設定或服務問題誤認為 Python 程式錯誤。這不是強制先發論壇的規則。[官方支援中心](https://www.ultralytics.com/support)

| 管道                                                                           | 要找的證據                             | 接著做什麼？                             |
| ------------------------------------------------------------------------------ | -------------------------------------- | ---------------------------------------- |
| [GitHub Issues：問題與提案](https://github.com/ultralytics/ultralytics/issues) | 重現資料、環境、維護者對預期行為的判斷 | 確認仍可重現，搜尋是否已有同題 PR        |
| [GitHub PRs：合併請求](https://github.com/ultralytics/ultralytics/pulls)       | 最終修改、後續修訂、合併或拒絕理由     | 讀最終結果，確認實際接受範圍             |
| [GitHub Discussions：討論區](https://github.com/orgs/ultralytics/discussions)  | 使用情境與長期問答                     | 找反覆出現、文件尚未解答的問題           |
| [官方論壇支援區](https://community.ultralytics.com/c/support/5)                | 使用者描述的症狀與修復確認             | 分辨套件、資料和 Platform 雲端服務的責任 |

自動歡迎訊息不代表維護者同意；`UltralyticsAssistant` 的訊息可能註明 automated（自動產生）。議題開啟、帶有錯誤標籤或沒有指定負責人，也不能單獨作為投入依據。

## 案例一：#26732 去重提示，先查先前方案為何未獲接受

**本書建議：暫不實作。** 先前有人鼓勵，不代表後續相同方案仍受歡迎。若要再投入，先核對被關閉 PR 的理由，或找到真正轉換錯誤的例子。

來源：[convert_coco silently drops duplicate annotations (identical output lines are de-duplicated without notice)](https://github.com/ultralytics/ultralytics/issues/26732)。建立日期為 2026-10-17；頁面顯示 Open、Feature（功能提案）。

**來源說了什麼：** Y-T-G 判定去重是預期行為，將錯誤標籤改為功能提案。10 月 19 日，pderrenger 曾建議在既有轉換流程計數。同日，一位參與者表示自己只增加日誌訊息的 PR 在審查後關閉，原因是新增程式碼不值得。這是參與者的轉述，本輪沒有獨立核對那筆 PR。

**從哪裡查：** `ultralytics/data/converter.py::convert_coco`。本地版本仍在輸出時用 `dict.fromkeys(map(tuple, rows))` 去重。

**下一步驗證：** 用小型 COCO JSON 標註檔，分別測試完全重複、相同框但分割標註不同，以及尺寸為零或負數的框。先定義哪些標註應保留，再比較輸出。輸出行數減少，不足以證明資料遺失。

## 案例二：#26707 保留整張分類圖片，先驗證現有做法

**本書建議：先查文件與範例是否有缺口，暫不新增參數。** 測試官方提供的擴充方式，再決定是否需要修正。

來源：[Classification crops away content on rectangular images, with no option to keep the full frame](https://github.com/ultralytics/ultralytics/issues/26707)。建立日期為 2026-10-16；頁面顯示 Open、Feature。

**來源說了什麼：** glenn-jocher 指出已有 `ClassifyLetterBox`（以補邊調整圖片的工具）。使用者可自行設定影像轉換流程，在訓練、驗證與推論時一致取代裁切。如果先補邊，後面卻仍裁切，就不能保證保留圖片邊緣。發問者表示會先測試。

**從哪裡查：** `ultralytics/data/augment.py` 的分類影像轉換，以及 `ultralytics/models/yolo/classify/` 的訓練、驗證與推論程式。

**下一步驗證：** 準備四角有標記的寬圖、長圖與正方形圖。保存三條流程真正送入模型的輸入，比對尺寸、色彩與正規化（調整像素數值的步驟）。如果文件有缺口，再提供最短可執行範例與圖片對照；只展示補邊前的圖片並不足夠。

**2026-10-29 驗證結果：預設載入下，現有文件範例已足夠，這題不再投入。** 照文件訓練後，訓練、驗證與從 `best.pt` 推論的輸入都保留四角標記；預設流程則四角全被裁掉。唯一落差出現在選用的安全載入模式，詳見[第四章的研究卡](roadmap.md#26707-card)。

## 案例三：#26324 預取與計時，有相符設備才投入

**本書建議：先查是否已有同題 PR，再決定是否測試。** 本地計時程式尚未涵蓋 MPS 同步，不代表沒有人正在修正。

來源：[Extend inference prefetch beyond CUDA: MPS, accelerator backends, CPU runtimes and videos](https://github.com/ultralytics/ultralytics/issues/26324)。glenn-jocher 於 2026-09-24 建立；頁面顯示 Open。

預取是模型計算時先準備下一批輸入。推論後端是執行模型的軟體；本題涵蓋 CUDA（NVIDIA GPU 運算平台）、MPS（Apple GPU 運算支援）及其他後端。

**來源說了什麼：** 維護者要求配對計時、相同輸出與硬體資訊。MPS 在 Air 與 Pro 的結果不同，因此不支持全面啟用。10 月 21 日，pderrenger 歡迎將 MPS 計時問題獨立做成小 PR。OpenVINO CPU 的預取則已由下一個案例完成。

**從哪裡查：** 計時位於 `ultralytics/utils/ops.py`，其中 `Profile` 的同步集合尚未包含 MPS。其他入口是 `ultralytics/engine/predictor.py` 的預取、`ultralytics/data/loaders.py` 的來源狀態，以及 `ultralytics/nn/backends/` 的後端選擇。本輪未全面核對待審 PR，不能直接宣稱此題可認領。

**下一步驗證：**

1. 使用真實設備，每次啟動獨立程序，固定資料、模型與每批輸入。
2. 交替測量原版與修改版，避免測量順序影響比較。
3. 除了各階段時間，也測量等待設備完成運算後的總耗時，以及等待本身的成本。
4. 逐筆比較輸出。影片還要檢查影格對齊、追蹤編號、提早停止與資源釋放。

不能只擴大啟用條件，就假設其他設備也會受益。

## 案例四：#26897 OpenVINO CPU 預取已合併，可用來學習審查範圍

**本書建議：讀懂這筆修改，不重做同一功能。** 它示範如何讓知道實際執行設備的模組決定是否預取，並檢查所有共用呼叫者。

來源：[Prefetch images during OpenVINO CPU inference](https://github.com/ultralytics/ultralytics/pull/26897)。頁面顯示 glenn-jocher 於 2026-10-26 合併。

**來源說了什麼：** OpenVINO 是模型推論工具。這筆 PR 只對明確使用 CPU 的 OpenVINO 後端啟用既有預取流程，不包括 `AUTO` 自動選擇設備或其他加速設備。作者提供配對計時與輸出相等檢查。

後續提交修正了 SAM 模型直接使用原始 `nn.Module`（PyTorch 模型物件）、沒有後端屬性的情況，也刪除重複測試。這表示初版通過自動審查後，仍可能需要修正。

**本地確認：** `ultralytics/nn/backends/openvino.py` 已有 `self.prefetch = device_name == "CPU"`；`ultralytics/engine/predictor.py` 已用帶預設值的 `getattr` 讀取屬性。

**下一步驗證：** 如果要研究其他後端，請重新測量該後端，不能套用 OpenVINO 的數字。

## 案例五：#26836 外部套件造成 CI 失敗，不要在模型程式補救

**本書建議：排除此題的 Python 修補方案。** 問題已指向外部套件，不應加入例外攔截、替代執行方式或永久版本限制來掩蓋原因。

來源：[Nightly Conda CI fails: conda-forge mkl 2026.2.0 is missing libmkl_gf_lp64.so.3](https://github.com/ultralytics/ultralytics/issues/26836)。glenn-jocher 於 2026-10-22 建立；頁面顯示 Open。

**來源說了什麼：** CI 是自動建置與測試流程。此題指出 Conda 套件環境中的 MKL 運算函式庫缺少檔案，原因在 conda-forge 發布的套件內容。議題明確表示 Ultralytics 專案無須修改，應等待套件修復與每日測試恢復，並附上套件建置專案的追蹤議題。

**下一步驗證：** 若要協助，請在指定 Linux Conda 環境核對套件版本、NumPy 能否載入，以及每日測試結果。Windows 不能直接驗證同一個共享函式庫缺檔問題。可交付的成果是環境重現紀錄，或確認外部修復已生效。

## 案例六：論壇 #2122 匯出問題已解決，可學習如何逐步定位

**本書建議：把它當成支援案例，不列入待修問題。** 遇到「export failed」（匯出失敗）時，先確認失敗發生在載入模型、轉換格式，還是服務部署。

來源：[Export error using the website](https://community.ultralytics.com/t/export-error-using-the-website/2122)。討論時間為 2026-07-16 至 07-19，使用者已確認成功。

**來源說了什麼：** 使用者在 Platform 雲端服務匯出分類模型失敗。團隊先取得任務、模型與專案資訊，再找到 Python 3.13 受限載入 checkpoint（儲存的模型檔）的問題。團隊回報已在 8.4.99 修正，也用該模型檔驗證服務端匯出。使用者後來確認可用。

**下一步驗證：** 遇到新案例，保存任務、模型檔來源、Python 與套件版本、匯出格式及完整錯誤。先確認能載入模型，再做最小匯出。不要預設重新訓練能解決，也不要要求使用者公開私人模型檔。

## 案例七：#26434 指標下降，先確認評分方式是否相同

**本書建議：先重現評估過程，不急著改訓練。** 議題仍帶錯誤標籤，不足以推翻後來的控制實驗。

來源：[Analysis of Accuracy Degradation on Small-Object Datasets Such as VisDrone in New Code Versions](https://github.com/ultralytics/ultralytics/issues/26434)。建立日期為 2026-09-29；頁面仍顯示 Open，但 10 月 2 日已有維護者實驗說明。

**來源說了什麼：** mAP 是彙整各類別 AP（平均精確度）的偵測評分。pderrenger 用相同評估程式替新舊訓練結果評分，指出落差與 AP 算法及 `max_det`（最多保留的偵測數）改變有關，不能直接解讀成新版訓練變差。討論也指出，舊版工作目錄若有未提交修改，會妨礙版本比較。

**從哪裡查：** `ultralytics/utils/metrics.py::compute_ap` 與 `ultralytics/models/yolo/detect/val.py`。若排除評估差異後仍能重現訓練差異，才往訓練流程、損失函數、參數更新方法與標註分配程式查。

**下一步驗證：** 固定初始權重、資料、隨機種子與環境，保存精確版本及工作目錄狀態。將兩版產生的模型檔交給同一評估程式，設定相同 `max_det`，再區分訓練差異與指標計算差異。

## 建議的投入順序

下表依驗證成本、維護者回覆、現有實作與設備需求排序，是本書判斷，不保證官方會接受。

| 優先順序 | 研究方向                                                    | 第一份成果                           | 繼續條件                                   |
| -------- | ----------------------------------------------------------- | ------------------------------------ | ------------------------------------------ |
| 1        | 分類影像轉換的文件或範例缺口                                | 訓練、驗證、推論的輸入對照與可跑範例 | 文件確有缺口，現有擴充方式可用             |
| 2        | MPS 各階段計時                                              | 真機同步前後計時與總耗時比較         | 有 Apple 設備、沒有重複 PR，並與參與者協調 |
| 3        | 其他後端或影片效能                                          | 配對測量與輸出一致性報告             | 有設備、改善穩定，且資源建立與釋放正常     |
| 暫停     | 轉換器只增加日誌提示                                        | 核對先前 PR 未獲接受的理由           | 發現新的轉換錯誤，或維護者改變結論         |
| 排除     | 已合併的 OpenVINO 預取、已修復的論壇匯出、外部 MKL 套件問題 | 理解既有修正與責任                   | 新版本出現新的可重現問題才重新研究         |

## 本章已查到哪裡

本輪已讀七個案例的主文與關鍵後續討論，也在 `bb3e1550d` 版本核對轉換器、分類影像轉換、`Profile`、推論流程與 OpenVINO 後端入口。沒有發文、認領議題、提出 PR 或執行模型實驗。

GitHub 命令列工具的額外搜尋曾受網路權限限制，因此沒有完整排除重複 PR。正式選題前仍需再查。

下一步：用[第四章研究卡](roadmap.md)記下來源、最後留言日期、預期行為、最小輸入、實際輸出、負責模組、既有 PR、設備與停止條件，再決定是否建立正式貢獻分支。
