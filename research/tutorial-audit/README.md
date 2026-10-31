# 教程執行結果：看輸入、流程、輸出與問題

每跑一個範例，就留下實際輸入、執行指令、輸出預覽，以及錯誤發生的位置。先看下面的結果，再用 [計畫](PLAN.md) 決定下一步；全部候選教程在 [逐頁清單](INVENTORY.md)。

| 已執行範例 | 輸入 → 流程 → 輸出 | 結果 | 問題 |
| --- | --- | --- | --- |
| [T01-A：安裝環境](records/T01.md#t01-a) | uv＋Python 3.13 → 安裝套件 → 可執行的 CPU 環境 | 通過 | 匯出版本清單曾因快取權限失敗，補設定後成功 |
| [T01-B：CLI 預測](records/T01.md#t01-b) | 兩張內建圖片＋模型 → 找出物件 → 兩張標示結果圖 | 通過 | 預設來源警告；權重位置待釐清 |
| [T01-C：Python 預測](records/T01.md#t01-c) | 圖片網址＋模型 → 預測並儲存 → 結果物件＋標示圖 | 通過 | 沒有阻塞錯誤；首次執行需要下載圖片 |
| [T02-A：指定來源與輸出](records/T02.md#t02-a) | 本機圖片＋conf=0.25 → CLI 預測 → 圖片與文字結果 | 通過 | 5 個框；無錯誤或警告 |
| [T02-B：提高信心門檻](records/T02.md#t02-b) | 相同輸入＋conf=0.85 → 篩選結果 → 圖片與分數比較 | 通過 | 剩 3 個框；圖上分數四捨五入可能造成誤解 |
| [T03-A：Python 結果讀取](records/T03.md#t03-a) | 本機圖片 → 讀取框、類別、分數 → 圖片、文字及 JSON | 通過 | 5 個框；座標換算、NumPy 轉換及新程序重跑均一致 |
| [T03-B：跨任務欄位探測](records/T03.md#t03-b) | 偵測結果 → 讀取分割 masks.data → AttributeError | 已重現預期錯誤 | masks 為 None；保留為教學說明候選，非已確認產品 bug |
| [T04-A：單圖來源](records/T04.md#t04-a) | 本機圖片 → list → 1 個 Results、5 框 | 通過 | 無錯誤或警告 |
| [T04-B：資料夾來源](records/T04.md#t04-b) | 兩張圖片 → list → 2 個 Results、5／3 框 | 通過 | 未測遞迴或混合來源 |
| [T04-C：影片 list](records/T04.md#t04-c) | 2 秒合成 AVI → 全部結果 → 10 影格影片 | 通過，有警告 | 記憶體累積警告 |
| [T04-D：影片 stream=True](records/T04.md#t04-d) | 同片 → 迭代 generator → 10 個結果與 AVI | 通過 | 迭代後才有輸出；結果與 list 一致 |
| [T05-A：設定持續性](records/T05.md#t05-a) | Python／CLI 更新 → 新程序讀取 → 設定相同 | 通過 | 無錯誤或警告 |
| [T05-B：目錄實際用途](records/T05.md#t05-b) | 設定三目錄 → 查找、預測、資料路徑解析 → 圖片與路徑證據 | 通過 | weights_dir 並非強制下載目的地 |
| [T05-C：重設設定](records/T05.md#t05-c) | 隔離設定 → CLI／Python reset → 新程序確認 | 通過 | reset 恢復預設；不是復原前一次修改 |
| [T06-A：CPU 短訓練](records/T06.md#t06-a) | COCO8＋預訓練模型 → 1 epoch → checkpoint、指標與圖表 | 調整執行權限後通過 | 首次下載受沙箱阻擋；單輪不能證明品質 |
| [T06-B：模型重載](records/T06.md#t06-b) | best.pt／last.pt → 新程序預測 → 各 5 框 | 通過 | 獨立訓練重跑結果相同；未驗證續訓 |
| [T07-A：獨立驗證](records/T07.md#t07-a) | T06 best.pt＋COCO8 val → 評估 → 指標與圖表 | 通過 | 與 T06 結尾完全一致；兩輪無警告 |
| [T07-B：指標讀取](records/T07.md#t07-b) | 驗證結果 → 逐圖／逐類別讀取 → JSON | 通過 | 逐圖門檻不同；maps 的未評估類別有填值 |
| [T08-A：預設追蹤](records/T08.md#t08-a) | 10 幀靜態短片 → TrackTrack → ID／影片 | 補裝依賴後通過 | 4 個 ID；首次自動安裝遇解碼錯誤 |
| [T08-B：切換追蹤器](records/T08.md#t08-b) | 相同短片 → ByteTrack → ID／影片 | 通過 | 5 個 ID；重跑相同，未評估真實運動 |
| [T09-A：ONNX 匯出](records/T09.md#t09-a) | 官方權重 → CPU 匯出 → ONNX | 通過 | uv 補齊依賴；兩輪無錯誤或警告 |
| [T09-B：重載比較](records/T09.md#t09-b) | 同圖、同尺寸 → PyTorch／ONNX → 5 框 | 通過 | 最大座標差約 0.000183 像素；未評估多圖品質 |
| [T10-A：格式 Benchmark](records/T10.md#t10-a) | 原始模型、COCO8 → PyTorch／ONNX → 指標與耗時 | 通過 | mAP 均 0.6693；本機 ONNX 較慢，原因未隔離 |
| [T10-B：獨立重跑](records/T10.md#t10-b) | 新程序與目錄 → 重測 → 成功狀態與指標核對 | 通過 | 無錯誤或警告；只有 4 張驗證圖 |
| [T11-A：notebook CLI 流程](records/T11.md#t11-a) | 本機圖、COCO8 → 預測／驗證／3 epochs 訓練／TorchScript → 圖片與模型 | 調整後通過 | TorchScript 棄用警告；未執行完整 COCO |
| [T11-B：notebook Python 流程](records/T11.md#t11-b) | 新模型 → 訓練／驗證／預測／ONNX → 指標、5 框與模型 | 兩輪通過 | 已釐清模型狀態與回傳型別；未執行 notebook kernel |
| [T12：分割物件去背](records/T12.md) | 三張圖＋seg 模型 → 照 Full Example 畫輪廓、去背 → 9 張 PNG | 通過 | 輪廓與模型遮罩 IoU 0.93–0.99；空輪廓會讓 drawContours 報錯，但約 400 個偵測中未出現 |
| [T13：直接用 COCO JSON 訓練](records/T13.md) | COCO8 轉 COCO JSON → COCOTrainer 訓練 1 epoch、改 JSON 重跑 → 指標與快取行為 | 通過 | 文件說相同大小的修改會沿用舊快取，實際會重新解析（#26283 加入修改時間）；PR #26960 |
| [T14：文件與程式的批次比對](records/T14.md) | 全部文件的 import、參數、連結＋221 個區塊實跑 → 與程式比對 → 落差清單 | 通過 | 2 個文件候選：`simple-utilities` 的 binary mask 說法與實際不符（0/255 會得到空標籤）；predict 來源表缺 `.txt`、`batch` 適用範圍不全（暫緩）；第一項已送 PR #26971 |

只有完成的案例會加入此表。未執行的範例不預填結果；同一頁只有部分案例完成時，整頁仍保留進行中。

每個案例都分清楚三種情況：**錯誤**讓某一步失敗；**警告**提醒你留意但可能仍成功；**待查問題**是觀察到的落差，還沒有證據判定為產品缺陷。
