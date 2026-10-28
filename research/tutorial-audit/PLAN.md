# 逐篇跑官方教程，找出值得貢獻的問題

這份計畫供你用 Windows、PowerShell 和 uv 逐篇驗證 Ultralytics 官方教程。每次完成一個可重現的小案例，留下結果、學習障礙及修正線索，再決定是否提出 issue 或 PR。

本計畫獨立於 `research/contributing` 書籍。先累積證據，不預設每篇教程都必須找出問題。

## 現在從哪裡開始

先開 [範例結果總覽](README.md)，查看已執行案例的輸入、流程、輸出圖片及問題。

1. T01–T11 第一輪選定案例已完成。下一輪從 Tasks 的 `docs/en/tasks/detect.md` 開始，先找出尚未驗證的範例，再依 segment → semantic → depth → classify → pose → obb 前進。
2. 下次先將選定範例編為 T12 並定義驗收範圍，再建立 `records/T12.md`。已完成案例不必重跑；T11 未執行儲存格仍保留未驗證。
3. 完成「每篇固定走七步」，更新 [結果總覽](README.md) 和 [逐頁清單](INVENTORY.md) 對應列的狀態與紀錄連結。
4. 下次從該紀錄的「下一步」接續；每次以一篇的一個範例為單位。

建立日期：2026-10-28。清單取自本 worktree，建立時 HEAD 為 `9662a727384611b7c28c2428ac252b7d57329b47`。官網可能領先或落後於這份原始碼，每次執行都另記日期、文件來源與套件版本。

先前的 pytest 圖片測試不計入教程驗證。2026-10-28 已完成 [T01：uv／CPU 安裝與 CLI、Python 首次預測](records/T01.md)、[T02：本機圖片與 CLI 門檻比較](records/T02.md) 及 [T03：Python 偵測結果讀取](records/T03.md)。T03 另保留跨任務讀取 masks 的失敗探測；文件改善候選仍待查證。上述教學頁的其他案例尚未全部驗證。

T04 已完成 [單圖、資料夾與短影片](records/T04.md)，list／generator 與新程序重跑結果一致。影片 list 的記憶體警告已記錄。

T05 已完成 [Settings 持續性、目錄解析與 reset](records/T05.md)，首次及新設定目錄重跑各 9 步通過。T01 的權重位置疑問已釐清：cwd 優先，weights_dir 可查找既有權重，並非強制下載目錄。文件候選仍待上游查重。

T06 已完成 [COCO8 CPU 單輪訓練與 checkpoint 重載](records/T06.md)。首次下載受沙箱權限阻擋，允許網路後成功；獨立目錄重跑的最終指標與預測摘要相同。模型位於專用 Temp 的 `t06-online/train/weights/`，下一項 T07 先確認 best.pt 仍存在。

T07 已完成 [獨立驗證與指標讀取](records/T07.md)，兩輪無錯誤或警告，指標與 T06 結尾驗證一致。已記錄逐圖統計門檻、maps 未評估類別填值，以及 CSV 差異仍未隔離唯一原因。下一項為 T08。

## 第一輪：先走完一條實際使用路徑

T11 已完成 [notebook 本機 CPU 選定流程](records/T11.md)。依原順序執行 6 格的調整版，兩輪均成功；3 epochs 訓練、驗證、預測、TorchScript／ONNX 匯出及重載有證據。TorchScript 三項棄用警告已記錄；Jupyter／Colab、完整 COCO、其他任務與附錄未執行。第一輪結束，下一輪從 Tasks detect 頁選定 T12 範例。

T10 已完成 [PyTorch／ONNX CPU Benchmark](records/T10.md)。兩輪成功且無警告，mAP50–95 均為 0.6693；PyTorch 約 29–36 ms／張，ONNX 約 315–317 ms／張。僅有 4 張驗證圖，未隔離速度差異原因，其他格式未執行。下一項為 T11。

T09 已完成 [ONNX CPU 匯出與重載比較](records/T09.md)。用 uv 補齊依賴後，兩輪均無錯誤或警告；單圖框座標最大差約 0.000183 像素，重跑預測相同。ONNX 檔案雜湊差異已確認只來自日期 metadata。下一項為 T10。

T08 已完成 [TrackTrack／ByteTrack 靜態短片追蹤](records/T08.md)。首次缺 lap，自動安裝遇到 cp950 解碼錯誤；用 uv 安裝後兩輪成功，逐幀 ID／座標一致。輸入與輸出影片已保存；真實運動、遮擋與離場品質未驗證。下一項為 T09。

以下是執行順序，不是官方課程編號。每列只先驗證指定案例；同頁其他分頁、參數組合及延伸範例仍待驗證。

| 編號 | 官方頁面／本機來源 | 這次要做什麼 | 完成時必須看見什麼 |
| --- | --- | --- | --- |
| T01 | [Quickstart](https://docs.ultralytics.com/quickstart/)；`docs/en/quickstart.md` | 在新 uv 環境安裝，執行第一個 CLI 與 Python 圖片預測 | 兩種入口正常結束，能找到結果圖片及 Python 結果物件 |
| T02 | [CLI](https://docs.ultralytics.com/usage/cli/)；`docs/en/usage/cli.md` | 指定本機圖片、輸出位置與一項參數 | 參數確實影響結果，能說出輸出存在哪裡 |
| T03 | [Python](https://docs.ultralytics.com/usage/python/)；`docs/en/usage/python.md` | 執行預測並讀取框、類別及信心分數 | 可對照圖片理解每個輸出欄位 |
| T04 | [Predict](https://docs.ultralytics.com/modes/predict/)；`docs/en/modes/predict.md` | 從單圖擴至資料夾、短影片，再看串流結果 | 每種來源均有合理結果，迭代串流時確實消費結果 |
| T05 | [Settings](https://docs.ultralytics.com/usage/settings/)；`docs/en/usage/settings.md` | 設定專用資料、權重和輸出目錄，重開程序驗證 | 設定持續有效，產物位置符合文件說明 |
| T06 | [Train](https://docs.ultralytics.com/modes/train/)；`docs/en/modes/train.md` | 使用教學的小型資料集，先做 CPU 短訓練 | 完成至少一個 epoch，產生可重新載入的 checkpoint |
| T07 | [Val](https://docs.ultralytics.com/modes/val/)；`docs/en/modes/val.md` | 驗證 T06 的模型並讀取指標 | 評估完成，知道資料切分、指標與結果檔位置 |
| T08 | [Track](https://docs.ultralytics.com/modes/track/)；`docs/en/modes/track.md` | 對可重用的短影片追蹤 | 可檢查跨影格 ID；記錄遮擋／離場造成的限制 |
| T09 | [Export](https://docs.ultralytics.com/modes/export/)；`docs/en/modes/export.md` | 先挑一個 Windows CPU 支援的格式匯出，再載入推論 | 匯出成功且可推論，記錄與原模型的差異 |
| T10 | [Benchmark](https://docs.ultralytics.com/modes/benchmark/)；`docs/en/modes/benchmark.md` | 限定已具備依賴的格式做比較 | 能解釋耗時、品質指標及不支援／跳過的項目 |
| T11 | `examples/tutorial.ipynb` | 依 notebook 原順序執行適用的儲存格 | 列出完成及未執行的儲存格，記錄 Colab 與本機差異 |

縮短訓練、指定 `device=cpu`、更換資料或將 Bash 改成 PowerShell，都要列入「調整」。短訓練只驗證流程，不能證明模型品質達標。CPU 路徑也不能代表 CUDA 路徑通過。

## 每篇固定走七步

### 1. 確定前提與成功條件

讀完即將執行的段落及其前置連結。記下輸入資料、依賴、作業系統、硬體、帳號與預期產物。先選定一個程式區塊或分頁，避免把「其中一段通過」寫成「整篇通過」。

教程若只有觀念說明，改以「能否完成它要求的決策或檢查」驗收，執行欄填「不適用」，不要虛報跑通。

### 2. 照原文跑，保留第一次結果

保留原始命令、工作目錄、完整錯誤、警告、退出碼及耗時。第一次失敗先記錄，再調整；安裝程序成功結束後才開始 import 或下一步。

uv 是本機環境管理方式。把原文 pip 安裝改為 `uv pip install --python ...` 時，要記錄這項轉換。若原文未提供 Windows 對應命令，記下缺少的內容。

### 3. 檢查教程是否教得順

- 每個步驟用到的檔案、變數與依賴，前面是否已準備？
- 複製指令後，是否知道應在哪個目錄或 shell 執行？
- 文件是否說明正常輸出，以及該去哪裡找結果？
- 出錯時，文件或錯誤訊息能否引導下一步？
- 做完後，能否用自己的話說明輸入、輸出與限制？

每個卡點都記「章節／程式區塊 → 當時預期 → 實際發生 → 補查什麼才繼續」。單純覺得難讀不足以形成修正依據。

### 4. 記下所有額外障礙，再分類

包含下載與權限、路徑含空白、Windows 多程序、依賴衝突、磁碟／記憶體、下載大小、耗時、GUI、影片編碼及未說明的帳號需求。成功但有警告、需要猜測或額外查詢，也要記。

把原因分為：文件缺漏、產品缺陷、第三方限制、本機環境、操作失誤或尚未確認。例如沙箱封鎖網路、跨磁碟複製較慢、安裝未完成就執行，不應直接判成 Ultralytics 的 bug。

### 5. 用最小調整跑通，再重跑確認

一次只改一個因素，記下每次調整及結果。分別填寫「原文結果」與「調整後結果」。找出解法後，以新程序及獨立輸出目錄重跑，確認不是依賴先前殘留的變數、檔案或套件。

連續 30 分鐘沒有新證據時，留下阻塞原因、已試方法與下一個驗證動作，再切換不依賴它的項目。這是安排時間的建議，不是宣告該教程無法執行。

### 6. 判斷是否值得貢獻

| 發現 | 下一個動作 |
| --- | --- |
| 步驟、依賴或輸出說明缺漏 | 在現有文件的對應段落補最小修正，避免另寫重複教程 |
| 支援情境下穩定重現的錯誤 | 縮成最小重現案例，定位負責行為的程式碼 |
| 錯誤訊息讓人無法採取行動 | 提出具體訊息及可行的下一步，附實際案例 |
| 未涵蓋的高風險回歸路徑 | 先查既有測試，再考慮最少的真實路徑測試 |
| 本機限制、操作失誤或已有清楚說明 | 留作個人紀錄；只有能證明普遍缺口時才提出上游修正 |
| 原因或適用版本仍不清楚 | 保留為待查，不急著開 PR |

提案前搜尋官方 issue、PR 和現有文件；確認在當時最新的 upstream main 是否仍存在。研究環境先保留，重現上游問題另開乾淨的功能 worktree。優先處理「常見流程受阻、證據完整、可小幅修正」的問題，不以新增測試數量或覆蓋率當目標。

### 7. 展示結果、更新進度並指定下一步

每個案例都必須交付以下內容，成功或失敗都要記：

- 輸入來源、模型、參數，以及可重跑的指令或腳本。
- 從準備到存檔的流程，標出錯誤發生在哪一步。
- 預期與實際輸出；圖片並排對照，數值說明欄位含義，影片提供代表影格及原檔位置。
- 錯誤、警告、教學卡點分開列出；沒有錯誤就明寫「無」，原因未確認就寫「待查」。
- 調整前後的結果、日誌連結、耗時、退出碼及未驗證範圍。

將展示用的證據存入研究目錄，確認圖片與連結可開啟，再更新結果總覽及逐頁清單。若要貢獻，填寫影響對象、最小修改位置、驗證方式及既有 issue／PR。正式 PR 使用自己的 fork 功能分支，目標為 `ultralytics/ultralytics:main`；個人掃描紀錄不放進上游 PR。

## T02 執行清單（已完成，保留供重跑）

1. 閱讀 `docs/en/usage/cli.md`，確認要驗證的官方範例與參數語法。
2. 使用 [T01 紀錄末尾](records/T01.md) 的命令恢復 uv 環境及設定。確認 Temp 內的環境、模型和圖片仍存在；若已清除，依版本清單重建並記錄。
3. 以本機 `bus.jpg`、`yolo26n.pt`、明確的 `project`／`name` 跑基準案例，保存獨立輸出。
4. 使用相同圖片及模型，只改 `conf` 信心門檻，另存結果；實際比較框數、分數和圖片，不預設改動一定造成差異。
5. 將兩次輸入、指令、輸出對照、錯誤／警告與解讀寫入 `records/T02.md`，證據放在 `records/T02-assets/`。確認這是本計畫的參數比較，標明與官方原例的差異。
6. 更新總覽與清單；把新發現留作候選，先不開 PR。T01 的權重目錄疑問保留給 T05。

## 後續如何逐步掃過全貌

1. **擴充任務**：按 `detect → segment → semantic → depth → classify → pose → obb`，逐項查看 Tasks 教學。每項先驗證推論，再挑支援的訓練／驗證範例；不要假設所有任務共用相同模型與指令。
2. **資料與訓練指南**：資料標註、COCO 轉換、資料增強、微調、指標及常見問題。用可公開的小資料集，檢查教學是否交代格式與切分。
3. **應用案例**：從 Guides 的計數、裁切、分割物件、熱圖等案例挑起，再查 `examples/` 的 Python 與 notebook。沿用同一段測試影片，分清範例差異。
4. **部署與進階整合**：ONNX／OpenVINO、SAHI、執行緒、客製 Trainer，接著才做 Docker、C++、Rust、服務部署。
5. **有前提才做的項目**：CUDA、TensorRT、Jetson、Raspberry Pi、雲端等。缺設備或帳號就填「待前提」及缺什麼；雲端先確認費用與資源清理方式。

[逐頁清單](INVENTORY.md) 是本機文件快照，包含候選教學及參考頁，並不聲稱每頁都能執行，也不涵蓋所有官方影片、歷史版本與外部課程。先篩選內容，再拆出頁內案例。每完成一輪，查看 [官方 Guides](https://docs.ultralytics.com/guides/)、[Quickstart](https://docs.ultralytics.com/quickstart/) 及 `examples/README.md`，補入新增教程。YOLOv5 等歷史專案另排一輪，避免混用版本。

## uv 環境與產物安排

保留現有 `.venv-local-test` 作為先前測試的環境。首次使用者路徑另建乾淨環境；同一組相容的教程可共用它，特殊匯出依賴另建環境。先固定發行版驗證，再用 editable 原始碼環境定位問題，兩種結果分開記。

首次環境可用以下命令建立。這是本計畫的 uv 配套，不是已驗證的官方原文：

```powershell
$repo = 'D:\tools\ultralytics\.worktrees\contribution-research'
$runRoot = Join-Path $env:TEMP ('ultralytics-tutorial-' + [guid]::NewGuid().ToString('N'))
$env:UV_CACHE_DIR = Join-Path $env:TEMP 'ultralytics-validation-uv-cache'
New-Item -ItemType Directory -Path $runRoot | Out-Null
Set-Location $runRoot
uv venv --python 3.13 .venv
# 上一步成功後才繼續；每一條命令都檢查 $LASTEXITCODE。
$python = Join-Path $runRoot '.venv\Scripts\python.exe'
uv pip install --python $python ultralytics --torch-backend cpu
# 安裝成功後，先指定專用設定目錄，再執行任何 Ultralytics import。
$env:YOLO_CONFIG_DIR = Join-Path $runRoot 'config'
& $python -c "import sys, torch, ultralytics; print(sys.version); print(torch.__version__); print(ultralytics.__version__); print(ultralytics.__file__)"
uv pip freeze --python $python | Set-Content -Encoding utf8 (Join-Path $runRoot 'requirements-resolved.txt')
```

記下 `$runRoot` 的實際值；重開 shell 後重新指定路徑及環境變數。接著按 Settings 文件設定專用 `weights_dir`、`datasets_dir`、`runs_dir`，在新程序確認，並記錄額外的前置動作。CLI 使用該環境的 `.venv\Scripts\yolo.exe`，Python 使用 `$python`，避免誤用全域版本。

命令、紀錄與可分享的最小案例放在本目錄；模型、資料集、虛擬環境、影片及完整日誌放專用執行目錄，不提交 Git。重要證據另行保存，Temp 可能被清除。分享日誌前移除金鑰、私人影像及個人路徑。

如果接著跑 pytest，必須使用專用工作目錄與權重目錄；測試結束時有檔案清理行為。教程執行成功和 pytest 通過是兩項不同證據。

## 每篇紀錄模板

複製以下內容到 `records/<編號>.md`。頁內有多個獨立範例時，各自建立小節與錨點，例如 T01-A、T01-B；內容過長再拆成獨立檔案。每個案例都先給讀者看輸入、流程、輸出與問題，再放詳細調查紀錄。

每次完成案例，同步更新 [結果總覽](README.md)。選取能說明結果的小型輸入／輸出圖片、實際腳本及整理過的日誌，保存到 `records/<編號>-assets/`，用相對連結展示。這些展示證據可保留在個人研究目錄；模型、完整資料集、虛擬環境及大型影片仍留在執行目錄。原始日誌與展示副本要區分，明說是否移除私人路徑或控制碼。尚未執行的案例只寫「未驗證」，不得填入預期值冒充實測。

```markdown
# T01：教程名稱／本次範例

- 狀態：未開始／進行中／待前提／受阻／已完成
- 官方 URL、本機文件路徑、章節或程式區塊：
- 文件查閱日期、文件 commit（若有）：
- 執行日期、OS／shell、CPU／GPU、Python／uv／torch／Ultralytics 版本：
- 安裝來源：PyPI 版本或 editable repo commit；是否有未提交變更：
- 環境、工作目錄、輸入資料來源、完整日誌及依賴快照位置：
- 本次範圍、未驗證的範例、成功條件：

## 範例展示（每個獨立範例各填一份）
- 案例編號與名稱：
- 一句話結果：成功／失敗／受阻／未執行，以及最重要的限制。
- 輸入：圖片、影片、資料、模型、來源連結及必要參數。
- 流程：準備 → 執行 → 檢查 → 存檔；附實際指令或可點開的腳本。
- 預期輸出與實際輸出：分開寫，附檔案連結、圖片對照或數值表。
- 如何讀結果：框、標籤、分數、欄位或指標代表什麼，不能證明什麼。
- Error（錯誤）：發生在哪一步、完整訊息、退出碼、是否阻塞；沒有就寫無。
- Warning（警告）：原始訊息、是否影響結果、是否需要處理。
- 教學卡點／待查問題：預期與實際的差異、證據、目前判斷。
- 解法與重跑：改了什麼、結果如何、仍未驗證什麼。
- 證據連結：輸入、輸出、日誌、版本及腳本；遺失的證據明確註明。

## 1. 跑通
- 原始指令或腳本：
- 原文結果：通過／失敗／未執行／不適用
- 退出碼、耗時、輸出產物、目視或數值檢查：

## 2. 教學順暢度
- 可直接完成／需要補查／無法繼續：
- 具體卡點、預期與實際、補查來源：

## 3. 其他障礙
| 發生步驟 | 錯誤／警告／困惑 | 影響 | 原因分類與證據 |
| --- | --- | --- | --- |
| 待填 | 待填 | 待填 | 尚未確認 |

## 4. 調整與重跑
- 每次只改了什麼、為什麼、結果：
- 調整後結果：通過／失敗／未執行
- 新程序重跑結果、殘留依賴或限制：

## 5. 貢獻候選
- 問題、受影響的人、最小重現方式：
- 已查過的文件／issue／PR 與查閱日期：
- 最新 upstream main 是否仍存在：未驗證／是／否
- 最小修改位置與驗證方式：
- 決定：不需貢獻／待查／文件修正／程式修正／回歸測試
- 對應 issue／PR（有才填）：

## 6. 下一步
- 下次直接執行的第一個動作：
- 缺少的前提與解除方式：
```

完成一篇的標準是：選定案例有結論、證據能找到、未涵蓋範圍已寫明，且貢獻候選已有處置。受阻項目保留原因，不列為跑通。
