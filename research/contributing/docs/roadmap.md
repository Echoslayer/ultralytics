# 4. 選一題，先完成可重現的驗證

**建議先調查 #26707 的分類前處理範例是否有缺口。** 你可以用自行產生的公開圖片，檢查圖片送入模型前的處理流程，較容易準備別人也能驗證的證據。

這不表示 #26707 已確認為程式錯誤。如果現有文件已說明完整，範例也能執行，就結束這題，不為提交修改而新增設定。[案例與維護者回覆](https://github.com/ultralytics/ultralytics/issues/26707)

第二個方向是 #26324 的計時與推論後端效能。推論後端指實際執行模型的軟體。其中 MPS 是 Apple GPU 的運算支援，需要 Apple 真機；目前工作目錄在 Windows，尚不能確認你有相符設備。OpenVINO CPU 預取已合併，請先查剩餘問題與同題 PR（合併請求）。[討論](https://github.com/ultralytics/ultralytics/issues/26324)；[已合併 PR](https://github.com/ultralytics/ultralytics/pull/26897)

這個排序是本書判斷。完整來源與排除理由見[案例章](issues-and-community.md)。

## 分四階段完成，不先承諾固定週數

| 階段            | 你要做什麼？                                     | 完成時留下什麼？                 | 何時停止或換題？                     |
| --------------- | ------------------------------------------------ | -------------------------------- | ------------------------------------ |
| A：查規範與版本 | 讀規範、記錄官方版本編號、查最新討論與 PR        | 一張來源完整的研究卡             | 已修復、已有同題 PR，或維護者不支持  |
| B：重現問題     | 固定輸入與環境，記錄預期與實際結果               | 可獨立執行的命令、輸入及結果     | 缺設備、無法替換私人資料，或無法重現 |
| C：做最小修正   | 找負責模組與所有呼叫者，列影響範圍，比較前後結果 | 小範圍修改與相關驗證             | 需要新介面或架構變更，先回提案討論   |
| D：正式貢獻     | 開乾淨分支、寫英文 PR、回覆審查                  | 對應遠端確切版本的驗證及審查紀錄 | 新結果推翻根因時，回到 B             |

#26707 已於 2026-10-29 完成階段 B，結論是停止，見下方[研究卡](#26707-card)。其他題目尚未執行 B、C、D。

## 第一個小型驗證：檢查分類圖片有沒有被裁掉

目標是確認寬圖與長圖的邊緣內容，在訓練、驗證、推論時是否符合選定的影像處理方式。這套驗證是本書建議，尚未執行。[#26707](https://github.com/ultralytics/ultralytics/issues/26707)

1. 準備寬圖、長圖與正方形圖，在四角放明顯標記。
2. 使用現行預設流程，保存真正送入模型前的數值陣列或其圖片呈現。
3. 改用官方建議的自訂影像轉換，在訓練、驗證與推論三條流程重做。
4. 比較三條流程的輸入，確認補邊後是否還有裁切，以及尺寸、色彩與像素數值處理是否一致。
5. 如果三條流程都能透過既有擴充方式達成，再搜尋文件是否已有完整範例。有缺口時才補最短範例。
6. 如果其中一條無法維持相同設定，先整理最小可重現範例，不直接新增全域參數。

只展示補邊結果會漏掉後續裁切；請以真正送入模型的內容作比較。

## 用研究卡記錄是否值得繼續

每次選題，可在本章末尾新增一節，填入以下欄位；暫時不需要新的自動追蹤工具。

```text
題目與來源網址：
最後讀到的留言日期、查核時間：
議題狀態、相關 PR、是否已有參與者：
基準 SHA（Git 版本編號）、套件版本、是否有未提交修改：
作業系統、Python、torch、推論後端、硬體：
預期行為及其規範來源：
最小公開輸入與執行命令：
實際輸出、錯誤或量測紀錄：
已排除的假設：
負責模組、呼叫者、受影響任務與模式：
最小修正方向：
驗證與停止條件：
決定：繼續、等待或排除；理由：
```

<a id="26707-card"></a>

### 研究卡：#26707 分類圖片裁切（已執行）

**結論：停止。在預設載入下，文件的「Custom transforms」範例已經讓訓練、驗證、推論三條流程都保留整張圖片，不需要修改文件或程式。**

```text
題目與來源網址：#26707 https://github.com/ultralytics/ultralytics/issues/26707
最後讀到的留言日期、查核時間：2026-10-16（發問者表示會測試）；查核 2026-10-29
議題狀態、相關 PR、是否已有參與者：Open；未見相關 PR；維護者已建議用自訂轉換
基準 SHA、套件版本、是否有未提交修改：cfc8e272c、ultralytics 8.4.191；研究分支有未提交的書稿修改，未改模型程式
作業系統、Python、torch、推論後端、硬體：Windows 11、Python 3.13、torch 2.14.1+cpu、PyTorch、CPU
預期行為及其規範來源：docs/en/tasks/classify.md「Custom transforms」：以 ClassifyLetterBox 取代裁切，保留整張圖片
最小公開輸入與執行命令：自行產生寬、長、方形灰圖，四角放 6px 色塊；
  python -I research/contributing/analysis/cls_letterbox_26707.py <輸出目錄>
實際輸出：
  - 預設 classify_transforms 處理寬圖：四角標記 0／4
  - 文件範例的驗證轉換：4／4
  - 訓練後從 best.pt 推論，送入模型的張量：4／4，形狀 1×3×64×64
  - 開啟 ULTRALYTICS_SAFE_LOAD=1 後載入同一 best.pt：失敗（TypeError）
已排除的假設：「best.pt 不會帶著自訂轉換，推論會退回裁切」——預設載入下不成立
負責模組、呼叫者：classify/train.py 把驗證轉換存進模型；classify/predict.py 沿用；
  nn/tasks.py 的安全載入允許清單只含 Compose、Normalize、Resize、CenterCrop、ToTensor
最小修正方向：無（預設路徑）。安全載入模式的錯誤訊息要求「使用官方模型」，對自訂轉換的使用者會誤導
驗證與停止條件：三條流程皆 4／4 → 停止
決定：排除。理由：文件已完整；安全載入是選用功能，另列為低優先觀察
```

結果檔：[cls-letterbox-26707.json](assets/cls-letterbox-26707.json)。實驗只訓練 1 輪、圖片 64 像素，目的只是檢查前處理，不評估準確率。實驗前請把 `YOLO_CONFIG_DIR` 指到暫存目錄；否則匯入 ultralytics 時，可能自動更新你全域的設定檔格式。

## 同時搜尋未解決議題、已合併修改與被拒方案

在官方 GitHub 專案貼上下列查詢，再加入元件名稱、症狀或錯誤字串。這些是搜尋範例；本輪沒有完整遍歷查詢結果。

```text
repo:ultralytics/ultralytics is:issue is:open label:bug
repo:ultralytics/ultralytics is:issue "ClassifyLetterBox"
repo:ultralytics/ultralytics is:pr "MPS" "Profile"
repo:ultralytics/ultralytics is:pr is:merged "prefetch"
repo:ultralytics/ultralytics is:issue is:closed "你的錯誤字串"
```

每輪讀一筆仍開啟的議題、一筆同領域已合併的 PR，再找已關閉或被拒的方案。這樣能同時看到使用者需求與維護者接受範圍。`good first issue`（適合首次參與的議題）標籤、留言數或修改行數，都不足以單獨決定是否投入。

## 選題起點的實測：照文件操作最有效

**照文件一步步操作，比挑程式寫探針更容易找到可送出的問題。** 2026-10-28 到 10-30，本書用幾種起點在官方 main 上找題目，結果如下：

| 起點 | 輪次 | 檢查範圍 | 可送出 |
| --- | --- | --- | --- |
| 照文件逐步操作 | T01–T11 | 安裝、預測、結果讀取、設定、訓練、驗證、追蹤、匯出、benchmark、notebook | 2 個 PR：#26935、#26955 |
| 未解決的 issue | #26707 研究卡 | 分類圖片裁切的延伸 | 1 個 PR：#26949 |
| 近期合併的 PR | R01、R02 | #26942、#26939、#26937，共 10 種用法 | 0 |
| 文件明寫的說法 | R03 | 五個任務頁的 Results 表格，`.pt` 與 ONNX 各一次 | 0 |
| 文件少提的組合 | R04 | FP16 ONNX、`rect` 驗證、OBB／pose 追蹤、靜態 ONNX 批次 | 0 |
| 未解決的 issue | R05 | #26795 大物體的分割遮罩 | 0（無法重現） |
| 照文件逐步操作 | T12 | `guides/isolating-segmentation-objects.md`，程式碼已在 #24701 修過 | 0 |
| 照文件逐步操作 | T13 | `guides/coco-json-training.md`，挑程式碼久未改動的頁 | 1 個文件修正（備妥未送） |

探針是只在本機跑的小腳本，用來確認某段程式在特定輸入下的行為。五輪探針都沒有找到可送出的缺陷，原因各不相同：

- **近期 PR：** 維護者合併前多半已在真實情境重新驗證；R01 唯一重現的副作用，是 PR 討論中已接受的取捨。
- **文件說法：** R03 與 R04 各有一個看似缺口的地方，查下去文件都已說明，只是寫在別頁：遮罩大小寫在 `docs/macros/predict-args.md`，靜態匯出的 `rect` 寫在 `export.md` 與 `val.md`。
- **issue：** 能在 CPU 上重現的 issue 已有人處理；沒人處理的，常缺重現資料。

照文件操作與 #26707 研究卡有效，共同點是走使用者真正會走的路徑，並把文件說法和實際結果放在一起比對。T05 的 `weights_dir`、T07 的 `metrics.box.maps`，以及照文件的自訂分類轉換在安全載入時失敗（#26949），都是這樣發現的。

探針仍然有用，但用途是確認與排除，不是找題目：照文件操作發現疑點後，再用探針隔離原因。寫探針時注意兩件事：

1. **先讀 PR 討論與相關文件，再下判斷。** 參數說明集中在 `docs/macros/`，不在任務頁。
2. **先印觀察，不急著寫斷言。** R01 誤把批次數當幀數，R04 沒發現多次匯出寫到同一個檔案，兩次都是先看輸出才抓到錯。

每輪的腳本、日誌與判斷見 `research/probe-audit/`。

## 重現後，用這份草稿整理留言或 PR

以下英文範本依序寫出環境、預期、實際結果、重現方式、可能原因、驗證與未檢查範圍。本輪沒有發送這份草稿。

```text
I reproduced <specific behavior> on <commit and environment> using <public input>.
Expected: <documented behavior>.
Observed: <actual output>.
To reproduce: <command or short snippet>.
The behavior appears to originate in <module or function>, because <evidence>.
Checks completed: <before/after result and related paths checked>.
Not yet checked: <specific platform or integration>.
```

先填完研究卡，再決定是否開始修正。是否採納，仍由維護者依實際修改、需求與維護成本判斷。
