# 2. 程式碼與驗證地圖

## 從使用者症狀反查 owner

Ultralytics 不只是偵測模型。研究基準的 task 順序為 `detect, segment, semantic, depth, classify, pose, obb`，模式為 `train, val, predict, export, track, benchmark`。同一個 engine 行為可能影響多個 task，因此「只驗一次 detect」不一定足以支持共用層修改。[cfg 定義](https://github.com/Echoslayer/ultralytics/blob/bb3e1550dbb819bd9846d4c99f368aebe8792a0e/ultralytics/cfg/__init__.py)

以下路徑以 repo 根目錄為基準；這是依 [AGENTS.md 的 owner 導覽](https://github.com/Echoslayer/ultralytics/blob/bb3e1550dbb819bd9846d4c99f368aebe8792a0e/AGENTS.md) 整理的閱讀順序，不表示已逐個函式完成程式碼審計。

| 症狀／領域                     | 先讀                                                                     | 追查時要注意                                        |
| ------------------------------ | ------------------------------------------------------------------------ | --------------------------------------------------- |
| 圖片、影片或 stream 輸入不一致 | `ultralytics/data/build.py`、`data/loaders.py`                           | 來源判定、batch、串流結束及資源釋放                 |
| 推論結果、輸出或儲存異常       | `ultralytics/engine/predictor.py`、`engine/results.py`                   | 共用流程與 task 專屬 postprocess 的邊界             |
| 標註轉換或資料載入             | `ultralytics/data/converter.py`、`data/dataset.py`、`data/utils.py`      | 類別索引、重複標註、空標註與 cache                  |
| 分類 resize／crop              | `ultralytics/data/augment.py`、`models/yolo/classify/`                   | 訓練與推論 preprocessing 必須一致評估               |
| 訓練、resume、DDP              | `ultralytics/engine/trainer.py`、`utils/torch_utils.py`、`utils/dist.py` | optimizer、EMA、多程序與設備狀態                    |
| mAP 或 validation 幾何         | `ultralytics/engine/validator.py`、`models/yolo/<task>/val.py`           | metric 契約、padding 與資料集差異                   |
| 匯出與 runtime                 | `ultralytics/engine/exporter.py`、`utils/export/`、`nn/backends/`        | 匯出成功與輸出等價是兩件事                          |
| CLI 與參數                     | `ultralytics/cfg/default.yaml`、`cfg/__init__.py`                        | 型別集合、deprecation、文件 macro 都受影響          |
| API reference                  | Python owner 的 docstring                                                | `docs/en/reference/` 多由工具生成，別直接修生成結果 |

最後一列的來源為 [docs/AGENTS.md](https://github.com/Echoslayer/ultralytics/blob/bb3e1550dbb819bd9846d4c99f368aebe8792a0e/docs/AGENTS.md)。

## 一次只追一條路徑

選好題後，先 `rg` 搜尋函式定義與所有呼叫點，再讀上下游。以 COCO 轉換為例，入口是 `convert_coco`；要確認輸入如何變成 YOLO 標註，以及去重發生在哪一層，才能判斷回報的是資料語意、既有政策或實作錯誤。此處只給閱讀方法，不預先宣告去重是 bug。[converter 原始碼](https://github.com/Echoslayer/ultralytics/blob/bb3e1550dbb819bd9846d4c99f368aebe8792a0e/ultralytics/data/converter.py)

```powershell
rg -n 'def convert_coco|convert_coco\(' ultralytics tests docs
rg -n 'classify_transforms|classify_augmentations' ultralytics tests
rg -n 'OMP_|set_num_threads|NUM_THREADS' ultralytics tests
```

以上是待研究時的搜尋命令，不是修正方案。不要只因一個全域 thread 設定能讓某次 benchmark 變快就提交，還要核對模型載入順序、同程序其他 backend 與 CPU／GPU 使用者。

## 驗證應隨變更範圍放大

| 改動範圍          | 最小合理驗證                           | 本輪狀態           |
| ----------------- | -------------------------------------- | ------------------ |
| 個人研究書        | 嚴格出版建置、頁面與內部連結、搜尋索引 | 屬於本輪交付檢查   |
| 文件中的指令／API | 在對應版本執行範例，核對 owner         | 未實作上游文件修正 |
| 資料轉換          | 小型公開輸入、輸出標註與相關既有測試   | 未重現候選 bug     |
| 共用 predictor    | 受影響 task／source／batch 模式        | 未執行模型測試     |
| export backend    | 對應隔離環境、真實 runtime、輸出品質   | 未安裝匯出環境     |
| CUDA／DDP         | 真實設備與多程序驗證                   | 未執行             |

不要在有重要檔案的目錄隨手跑 pytest。研究基準的 `tests/conftest.py` session cleanup 會刪除權重目錄中的部分匯出產物，也會清理 cwd 的特定檔案；應使用 scratch cwd 和專用權重目錄。`--export-env` 只篩選測試，不會安裝依賴。[測試清理程式](https://github.com/Echoslayer/ultralytics/blob/bb3e1550dbb819bd9846d4c99f368aebe8792a0e/tests/conftest.py)；[環境說明](https://github.com/Echoslayer/ultralytics/blob/bb3e1550dbb819bd9846d4c99f368aebe8792a0e/AGENTS.md)

## 容易誤踩的版本差異

這份基準使用 `quantize` 作為公開精度參數，`nms` 是 tri-state；較舊例子的 `half`、`int8`、`end2end` 不能直接抄成新的範例。正式修正時讀當時 checkout 的 `cfg`、docstring 與測試，不把搜尋到的歷史答案視為現行契約。[版本規則](https://github.com/Echoslayer/ultralytics/blob/bb3e1550dbb819bd9846d4c99f368aebe8792a0e/AGENTS.md)
