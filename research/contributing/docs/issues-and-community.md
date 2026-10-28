# 從 issue 與社群找到值得做的貢獻

研究日期：2026-10-28。以下是本輪讀到的官方 GitHub 與論壇頁面快照，不是完整待辦清單，也不是已認領工作。網頁擷取可能有數日快取；表中的 Open／Merged 是頁面顯示狀態，正式選題前要再讀最新留言與相關 PR。所有「建議」與「驗證門檻」都是本書的研究判斷，本輪沒有重跑模型實驗。

## 先找對討論入口

官方支援入口將文件、論壇／Discord 與 GitHub 問題回報列為不同管道。實務上，先在論壇釐清使用方式，再將能獨立重現的套件問題整理到 GitHub，能減少把設定或服務端問題誤當 Python bug 的機會。這個工作順序是本書建議，並非強制先發論壇。[官方支援中心](https://www.ultralytics.com/support)

| 管道                                                                  | 研究時要找的證據                       | 下一步                             |
| --------------------------------------------------------------------- | -------------------------------------- | ---------------------------------- |
| [GitHub Issues](https://github.com/ultralytics/ultralytics/issues)    | 重現資料、環境、維護者對預期行為的判定 | 核對是否仍可重現，並搜尋重複 PR    |
| [GitHub PRs](https://github.com/ultralytics/ultralytics/pulls)        | 最終 diff、後續修訂、合併或拒絕理由    | 學習實際接受範圍，避免只看最初提案 |
| [GitHub Discussions](https://github.com/orgs/ultralytics/discussions) | 使用情境、文件頁的長期問答             | 找反覆出現且文件尚未解答的問題     |
| [官方論壇 Support](https://community.ultralytics.com/c/support/5)     | 實際使用者如何描述症狀、是否已確認修復 | 分辨套件、資料與 Platform 服務責任 |

不要把自動歡迎訊息視為維護者承諾；`UltralyticsAssistant` 的訊息可能明確註記 automated。也不要把 Open、bug label 或沒有 assignee 當成「可以直接做」的證據。下面的案例顯示，這些訊號可能落後於討論內容。

## 七個實際案例

### 1. #26732：轉換器去重提示，為什麼小改也可能不值得合併

[convert_coco silently drops duplicate annotations (identical output lines are de-duplicated without notice)](https://github.com/ultralytics/ultralytics/issues/26732)，2026-10-17 建立；頁面顯示 Open、Feature。

**來源事實：** Y-T-G 判定去重是預期行為，將 bug 改為 feature。10 月 19 日 pderrenger 曾建議將計數留在既有轉換流程；同日參與者又回報，自己的 logging-only PR 在審查後被關閉，理由是增加的程式碼不值得。後者是參與者對審查結果的轉述，本輪未獨立核對該 PR。

**本書判斷：暫不實作。** 這是「讀到最後一則留言」的重要案例。先前有鼓勵，不代表後續相同方案仍受歡迎。若要再投入，應找到實際錯誤轉換，或先核對被關閉 PR 的具體理由。

**追查 owner：** `ultralytics/data/converter.py::convert_coco`。本地快照仍在既有輸出步驟以 `dict.fromkeys(map(tuple, rows))` 去重。

**驗證門檻：** 小型 COCO JSON 分別覆蓋完全重複、相同框但不同 segmentation、非正尺寸框；先界定應保留的語意，再比較輸出，不能因為輸出行數減少就判定資料遺失。

### 2. #26707：分類保留整張圖片，先用既有擴充點

[Classification crops away content on rectangular images, with no option to keep the full frame](https://github.com/ultralytics/ultralytics/issues/26707)，2026-10-16 建立；頁面顯示 Open、Feature。

**來源事實：** glenn-jocher 指出已有 `ClassifyLetterBox`；目前可用 custom transforms 在 train、val、predict 一致取代裁切。單純先補邊、仍保留後續 crop，不能保證邊緣特徵留住。發問者表示會先測此方案。

**本書判斷：適合文件與重現研究，尚不足以新增參數。** 先驗證官方擴充模式是否完整解決情境；若有缺口，優先提供最短可執行範例及影像對照。

**追查 owner：** `data/augment.py` 的分類 transforms，以及 `models/yolo/classify/` 的 trainer、validator、predictor；路徑均相對 `ultralytics/`。

**驗證門檻：** 用四角帶標記的寬、長、正方形圖像，逐一保存三條路徑真正送入模型的輸入，核對尺寸、色彩與正規化。文件修改也必須跑通範例，不能只展示補邊前的圖片。

### 3. #26324：效能方向明確，但每個 backend 都需要證據

[Extend inference prefetch beyond CUDA: MPS, accelerator backends, CPU runtimes and videos](https://github.com/ultralytics/ultralytics/issues/26324)，glenn-jocher 於 2026-09-24 建立；頁面顯示 Open。

**來源事實：** 維護者要求配對計時、相同輸出與硬體資料。MPS 的 Air／Pro 測量呈現不同結果，維護者不支持直接全面啟用。10 月 21 日 pderrenger 歡迎將 MPS 計時問題獨立做成小 PR。OpenVINO CPU 部分後來已由下節 PR 完成。

**本書判斷：有設備才進入候選。** MPS 計時值得先查重；本地 `utils/ops.py::Profile` 的同步集合尚未包含 MPS，但這不代表上游沒有待審 PR。本輪未完成待審 PR 的全面核對，不能宣稱可直接認領。

**追查 owner：** 計時在 `ultralytics/utils/ops.py`；預取在 `engine/predictor.py`，資料來源狀態在 `data/loaders.py`，backend 選擇在 `nn/backends/`。

**驗證門檻：** 使用真實硬體與獨立新程序，交替執行基準／候選，固定資料、模型與 batch。除了階段計時，量測同步後的總耗時及同步成本；逐筆比較輸出。影片須另驗證 frame 對齊、追蹤 ID、提早停止及資源釋放，不能只擴大條件式。

### 4. #26897：已合併的性能貢獻，如何把範圍縮到可驗收

[Prefetch images during OpenVINO CPU inference](https://github.com/ultralytics/ultralytics/pull/26897)，頁面顯示 2026-10-26 由 glenn-jocher 合併。

**來源事實：** PR 僅讓明確使用 CPU 的 OpenVINO backend 選用既有預取路徑，排除 AUTO 與其他 accelerator。作者提供配對計時和輸出相等檢查。後續 commit 修正 SAM 使用原始 `nn.Module` 而沒有 backend 屬性的問題，也移除重複測試。

**本書判斷：歷史範本，不再做同一功能。** 可學習的不是「加一個 flag」，而是讓知道實際執行裝置的 owner 決定資格，並檢查所有共用 caller。初版通過自動審查仍可能需要修正。

**本地確認：** `ultralytics/nn/backends/openvino.py` 已有 `self.prefetch = device_name == "CPU"`；`engine/predictor.py` 已使用帶預設值的 `getattr`。

**後續門檻：** 若主張其他 backend 也能受益，重新建立該 backend 的證據，不能套用 OpenVINO 的數字。

### 5. #26836：CI 失敗，但正確貢獻可能是不改 repo

[Nightly Conda CI fails: conda-forge mkl 2026.2.0 is missing libmkl_gf_lp64.so.3](https://github.com/ultralytics/ultralytics/issues/26836)，glenn-jocher 於 2026-10-22 建立；擷取頁面顯示 Open。

**來源事實：** 問題描述將原因定位到 conda-forge 的 MKL 套件內容，並明確表示此 repository 無須修改；等待上游修復與 nightly 恢復。該頁也連到 feedstock 的追蹤問題。

**本書判斷：排除 Python 修補。** 不應在 import 或推論層加 catch、fallback 或永久 pin 來掩蓋已知外部 packaging 問題。

**驗證門檻：** 在問題所指的 Linux Conda 環境確認套件版本、NumPy import 與 nightly 結果；Windows 上無法直接驗證同一共享函式庫失敗。若提供協助，交付可核對的環境重現或上游修復確認即可。

### 6. 論壇 #2122：從模糊匯出錯誤到使用者確認修復

[Export error using the website](https://community.ultralytics.com/t/export-error-using-the-website/2122)，2026-07-16 至 07-19 的討論；內容已由使用者確認成功。

**來源事實：** 使用者在 Platform 匯出分類模型失敗。團隊先取得 task、模型及專案資訊，再定位 Python 3.13 的 restricted checkpoint loading，回報修正在 8.4.99，並用該 checkpoint 驗證服務端匯出。使用者其後確認可用。

**本書判斷：已解決的支援案例。** 適合學習問診順序，不列為待修 bug。看到「export failed」時，先確認失敗發生在載入 checkpoint、轉換格式或服務部署哪一層。

**驗證門檻：** 新案例須保留 task、來源 checkpoint、Python／套件版本、格式與完整錯誤；先驗證能否載入，再跑最小匯出。不能以重新訓練作為預設解法，也不能要求使用者公開私有 checkpoint。

### 7. #26434：mAP 下降可能來自評估定義

[Analysis of Accuracy Degradation on Small-Object Datasets Such as VisDrone in New Code Versions](https://github.com/ultralytics/ultralytics/issues/26434)，2026-09-29 建立；頁面仍顯示 Open，10 月 2 日已有維護者實驗說明。

**來源事實：** pderrenger 將新舊訓練結果交由相同 evaluator 評分，指出看到的落差與 AP 計算及 `max_det` 改變相關，不能直接解讀為新訓練退化。討論亦指出舊 checkout 的 dirty 狀態會妨礙版本比較。

**本書判斷：以重現方法學為主，先不改 loss／optimizer。** issue 的 bug label 不足以推翻後來的控制實驗。

**追查 owner：** `ultralytics/utils/metrics.py::compute_ap` 與 `models/yolo/detect/val.py`；若之後仍有可重現訓練差異，才往 trainer、loss 與 assigner 查。

**驗證門檻：** 固定初始權重、資料、seed 與環境，保存精確 commit 和工作樹狀態；將兩版產生的 checkpoint 用同一 evaluator、相同 `max_det` 評估，再分離訓練差異與計算指標差異。

## 目前的投入順序

以下優先順序是本書推論，依據是驗證成本、維護者訊號、是否已有實作，以及本地是否能取得必要硬體；不是保證會被接受的題目清單。

| 順序 | 研究方向                                                    | 第一份可交付成果                       | 繼續投入的條件                                 |
| ---- | ----------------------------------------------------------- | -------------------------------------- | ---------------------------------------------- |
| 1    | 分類 custom transforms 的文件／範例缺口                     | train／val／predict 輸入對照與可跑範例 | 現有文件確有可指認的缺口，且既有擴充點可用     |
| 2    | MPS 階段計時                                                | 真機同步前後計時與總耗時差異           | 有 Apple 硬體、查無重複 PR，並與既有參與者協調 |
| 3    | 未完成 backend／影片效能研究                                | 配對 benchmark 與輸出一致性報告        | 有相關硬體，改善穩定且未破壞資源生命週期       |
| 暫停 | converter logging-only                                      | 先核對被拒 PR 的理由                   | 出現新的實際轉換錯誤或新的維護者結論           |
| 排除 | 已合併 OpenVINO CPU 預取、已修復論壇匯出、外部 MKL 包裝問題 | 讀懂既有修正與責任邊界                 | 僅在新版本出現新的可重現問題時重開研究         |

選定方向後，先保存一張研究卡：來源連結、最後讀到的留言日期、預期行為、最小輸入、現行輸出、owner、既有 PR、驗證設備、停止條件。先完成這張卡，再決定是否建立真正的貢獻分支。

## 本章查核範圍

已讀各案例的主文與關鍵後續討論，並在本地 `bb3e1550d` 快照核對 converter、分類 transforms、Profile、predictor 與 OpenVINO backend 的相關入口。本輪沒有發文、認領 issue、提出 PR 或執行上述模型實驗。GitHub CLI 的額外搜尋曾受本機網路權限限制，因此未宣稱已排除所有重複 PR；正式選題前仍須重新查核。
