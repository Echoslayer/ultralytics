# 2. 從症狀找到負責模組

**先找直接控制問題行為的模組，再查它影響哪些功能。** 共用程式可能服務多種模型任務，只測一次物件偵測，不一定足以驗證共用層修改。

研究版本定義的任務順序為 `detect, segment, semantic, depth, classify, pose, obb`，依序代表物件偵測、實例分割、語意分割、深度估計、分類、姿態估計與旋轉框偵測。操作模式順序為 `train, val, predict, export, track, benchmark`，即訓練、驗證、推論、匯出、追蹤與效能測試。[cfg 定義](https://github.com/Echoslayer/ultralytics/blob/bb3e1550dbb819bd9846d4c99f368aebe8792a0e/ultralytics/cfg/__init__.py)

## 按症狀查檔案

下表的路徑都相對於 `ultralytics/` 資料夾。內容依 [AGENTS.md 的模組導覽](https://github.com/Echoslayer/ultralytics/blob/bb3e1550dbb819bd9846d4c99f368aebe8792a0e/AGENTS.md) 整理；本輪沒有逐一審查所有函式。

| 症狀                           | 先讀的檔案                                                   | 需要注意什麼？                           |
| ------------------------------ | ------------------------------------------------------------ | ---------------------------------------- |
| 圖片、影片或串流輸入不一致     | `data/build.py`、`data/loaders.py`                           | 來源判定、每批輸入、串流結束與資源釋放   |
| 推論結果、輸出或儲存異常       | `engine/predictor.py`、`engine/results.py`                   | 共用流程與各任務後處理的分工             |
| 標註轉換或資料載入異常         | `data/converter.py`、`data/dataset.py`、`data/utils.py`      | 類別編號、重複標註、空標註與快取         |
| 分類圖片縮放或裁切不符預期     | `data/augment.py`、`models/yolo/classify/`                   | 訓練與推論前的圖片處理是否一致           |
| 訓練、續訓或多設備訓練異常     | `engine/trainer.py`、`utils/torch_utils.py`、`utils/dist.py` | 參數更新、移動平均權重、多程序與設備狀態 |
| 準確度指標或驗證圖片尺寸有差異 | `engine/validator.py`、`models/yolo/<task>/val.py`           | 指標定義、圖片補邊與資料集差異           |
| 模型匯出或執行異常             | `engine/exporter.py`、`utils/export/`、`nn/backends/`        | 匯出成功後，執行結果是否仍一致           |
| 命令列或參數異常               | `cfg/default.yaml`、`cfg/__init__.py`                        | 參數型別、舊參數轉換與共用文件片段       |
| 程式介面參考頁有錯             | 對應 Python 函式或類別的 docstring（程式內說明文字）         | 參考頁多由工具生成，應修改來源說明       |

多設備訓練常稱 DDP（分散式資料平行訓練）；移動平均權重常稱 EMA。查看程式碼時會遇到這些縮寫。參考頁規則見 [docs/AGENTS.md](https://github.com/Echoslayer/ultralytics/blob/bb3e1550dbb819bd9846d4c99f368aebe8792a0e/docs/AGENTS.md)；其生成目錄位於專案根目錄的 `docs/en/reference/`。

## 搜尋定義，也搜尋誰會呼叫它

選題後，用 `rg`（搜尋檔案內容的命令）找出函式定義與所有呼叫位置，再讀輸入與輸出流程。

例如，COCO 是一種影像標註資料格式，轉換入口是 `convert_coco`。先看它如何產生 YOLO 標註，再找出移除重複資料的位置。這樣才能判斷問題出在資料意義、既有處理規則，還是程式錯誤；不能先認定去重就是錯誤。[轉換器原始碼](https://github.com/Echoslayer/ultralytics/blob/bb3e1550dbb819bd9846d4c99f368aebe8792a0e/ultralytics/data/converter.py)

在專案根目錄執行：

```powershell
rg -n 'def convert_coco|convert_coco\(' ultralytics tests docs
rg -n 'classify_transforms|classify_augmentations' ultralytics tests
rg -n 'OMP_|set_num_threads|NUM_THREADS' ultralytics tests
```

這些命令用來找線索，不是修正方案。假設調整全域執行緒設定讓一次測量變快，你仍要查模型載入順序、同一程序內的其他推論後端（實際執行模型的軟體），以及 CPU 與 GPU 使用情境。

## 修改影響越廣，驗證範圍也越大

| 改了什麼？         | 至少要驗證什麼？                     | 本輪狀態         |
| ------------------ | ------------------------------------ | ---------------- |
| 個人研究書         | 嚴格建置、頁面與內部連結、搜尋索引   | 本輪出版檢查範圍 |
| 文件指令或程式介面 | 在對應版本執行範例，核對負責模組     | 未修改官方文件   |
| 資料轉換           | 小型公開輸入、輸出標註與相關既有測試 | 未重現候選問題   |
| 共用推論流程       | 受影響任務、來源類型與每批輸入模式   | 未執行模型測試   |
| 匯出後端           | 對應隔離環境、真實執行軟體與輸出品質 | 未安裝匯出環境   |
| CUDA 或 DDP        | 真實設備與多程序行為                 | 未執行           |

CUDA 是 NVIDIA GPU 的運算平台。這類設備相關修改，不能只靠模擬環境驗證。

執行 pytest（Python 測試工具）前，請準備空的臨時工作目錄與專用權重目錄。研究版本的 `tests/conftest.py` 會在測試結束時清理部分匯出產物，也會刪除當前工作目錄中的特定檔案。不要從存有重要檔案的目錄執行。另需注意，`--export-env` 只篩選測試，不會安裝套件。[測試清理程式](https://github.com/Echoslayer/ultralytics/blob/bb3e1550dbb819bd9846d4c99f368aebe8792a0e/tests/conftest.py)；[環境說明](https://github.com/Echoslayer/ultralytics/blob/bb3e1550dbb819bd9846d4c99f368aebe8792a0e/AGENTS.md)

## 使用當前版本的參數，不直接照抄舊範例

研究版本以 `quantize` 指定公開精度參數。`nms` 有三種設定值（`None`、`True`、`False`），各自代表不同處理方式。舊範例的 `half`、`int8`、`end2end` 不應直接複製成新範例。

正式修正前，請讀當時版本的 `cfg`、程式內說明與測試，確認預期行為。[版本規則](https://github.com/Echoslayer/ultralytics/blob/bb3e1550dbb819bd9846d4c99f368aebe8792a0e/AGENTS.md)

下一步：到[案例章](issues-and-community.md)選一個症狀，用本章表格找到閱讀起點。
