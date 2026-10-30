# 1. 準備一筆小型貢獻

**先證明問題，再修改程式。** 一份可公開重現的回報，或一個能指出文件錯誤的範例，都能幫維護者判斷下一步。官方也接受文件修改與 PR 審查（檢查別人的合併請求）。[貢獻入口](https://docs.ultralytics.com/help/contributing/)

## 先確認你要交付哪一種成果

| 貢獻類型 | 你要準備的證據                               | 遇到這些情況先停下來                         |
| -------- | -------------------------------------------- | -------------------------------------------- |
| 錯誤修正 | 修改前能重現，修改後符合預期，原有功能仍正常 | 只有私人模型權重，或還不清楚預期行為         |
| 文件修正 | 文件原句、對應程式碼與可執行範例             | 只改自動生成的參考頁，未改來源說明           |
| 效能改善 | 相同設備、輸入、精度與輸出品質下的比較       | 只有單次計時，或改了全域設定卻未驗證其他功能 |
| 功能提案 | 多位使用者的需求、現有介面的限制與維護者同意 | 只適用自己的流程，且需要新增參數或套件       |
| 協助排查 | 環境資訊、最小輸入與可排除的假設             | 尚未查證就將使用問題判定為程式錯誤           |

上表是本書的執行建議，依據為 [CONTRIBUTING.md](https://github.com/ultralytics/ultralytics/blob/main/CONTRIBUTING.md) 和本地研究版本的 [AGENTS.md](https://github.com/Echoslayer/ultralytics/blob/bb3e1550dbb819bd9846d4c99f368aebe8792a0e/AGENTS.md)。

## 修改範圍要小，不能只看新增行數

兩份規範計算修改量的方式不同：

- `CONTRIBUTING.md`：首次貢獻若約超過 50 行實質修改，通常不受鼓勵；文件、程式內說明文字（docstring）與格式修改可例外處理。
- `AGENTS.md`：超過 50 行「淨新增非文件程式碼」，或加入新參數、新依賴套件，都需要更強的理由。

因此，淨新增 49 行並不保證通過。請讓修改只解決一個問題，保留完整解法，並能說明為何無法再縮小。[範圍規範](https://github.com/ultralytics/ultralytics/blob/main/CONTRIBUTING.md)；[研究版本規則](https://github.com/Echoslayer/ultralytics/blob/bb3e1550dbb819bd9846d4c99f368aebe8792a0e/AGENTS.md)

測試規則也要一起看。一般貢獻指南要求適當驗證；本地代理規範則預設不新增測試，只有既有測試未覆蓋且風險高的路徑才補最少測試。先找既有測試並執行真實功能，不要只為增加測試數量而大量模擬設備或環境。

## 按七個步驟準備修正

1. **搜尋是否已有解法。** 查相同症狀、已關閉議題與正在審查的 PR，並讀結案理由。
2. **記錄版本。** 保存基準 SHA（Git 用來識別版本的編號），確認個人副本與官方專案是否同步。
3. **縮小重現範例。** 使用可公開分享的輸入，寫下預期結果、實際結果和完整錯誤。
4. **找到負責模組。** 搜尋所有呼叫它的程式，在直接控制或觀察行為的位置修正。不要靠下游例外處理或初始化旗標掩蓋問題。
5. **列出受影響範圍。** 包括模型任務、操作模式、平台、輸出格式與文件，再實作最小修正。
6. **驗證修改前後。** 跑相關既有檢查並保留結果。效能題還要確認輸出品質。
7. **準備小型 PR。** 說明問題、行為變化與驗證結果，再回覆自動工具和人工審查。

前 3 步呼應[官方最小可重現範例方法](https://docs.ultralytics.com/help/minimum-reproducible-example/)。負責模組與最小修改原則來自 [AGENTS.md](https://github.com/Echoslayer/ultralytics/blob/bb3e1550dbb819bd9846d4c99f368aebe8792a0e/AGENTS.md)。

## 正式修正另開分支，研究書留在原處

**把修改推到個人副本的功能分支，再向官方 `main` 提出 PR。** 推送是上傳提交；PR 是請官方審查並合併，兩者的目的地不同。

| 用途                           | 專案                                             | 分支              |
| ------------------------------ | ------------------------------------------------ | ----------------- |
| 取得官方最新程式，作為修正起點 | `ultralytics/ultralytics`（遠端名稱 `upstream`） | `main`            |
| 上傳自己的修改                 | `Echoslayer/ultralytics`（遠端名稱 `origin`）    | 例如 `fix/my-fix` |
| 請官方接收修改                 | `ultralytics/ultralytics`                        | `main`            |

`origin` 和 `upstream` 只是本機為遠端網址取的名字。先用 `git remote -v` 核對網址，不要只看名字。官方的開發與實驗分支不是一般貢獻的預設入口；除非維護者另有指定，請以官方 `main` 為起點與 PR 目標。

目前 `origin` 指向你的個人副本：`https://github.com/Echoslayer/ultralytics.git`。研究分支從 `origin/main` 建立，原本的工作目錄仍保留。

準備正式貢獻時：

1. 執行 `git remote -v`，查看遠端來源。
2. 如果尚未設定官方來源，新增名為 `upstream` 的遠端來源，再用 `fetch` 取得官方版本。
3. 確認個人副本沒有獨有提交，將遠端 `main` 快轉同步到官方 `main`，再從更新後的 `origin/main` 建立功能分支與工作樹。
4. 只帶入該題需要的修正，不帶入整本研究書或出版套件。

每個正式修正使用獨立分支。推送前先拉取遠端更新並 `rebase`（將自己的提交接到更新後的版本上）。官方自動工具可能加入格式或標頭提交，請保留他人的修改。[工作樹與審查規則](https://github.com/Echoslayer/ultralytics/blob/bb3e1550dbb819bd9846d4c99f368aebe8792a0e/AGENTS.md)

2026-10-29 已依使用者指示同步 `Echoslayer/main`，並推送獨立的文件功能分支，見下方實例。主目錄的本地 `main` 沒有隨遠端同步自動移動。

### PowerShell 操作範例

以下命令供正式修正時使用。`my-fix` 是範例名稱，請換成新的分支與目錄名稱。每一步成功後再執行下一步。

1. 回到主目錄並核對遠端：

   ```powershell
   Set-Location D:\tools\ultralytics
   git remote -v
   ```

2. 如果尚未設定 `upstream`，新增官方網址；已設定且網址正確就跳過：

   ```powershell
   git remote add upstream https://github.com/ultralytics/ultralytics.git
   ```

3. 取得兩邊版本，先確認是否能安全同步：

   ```powershell
   git fetch upstream main
   git fetch origin main
   git rev-list --left-right --count origin/main...upstream/main
   ```

   若輸出是 `0 N`，表示個人副本沒有獨有提交、落後官方 N 筆，可在 GitHub 個人副本頁面使用 **Sync fork → Update branch**。若左側不是 0，先檢查分歧，不要強制覆蓋。同步成功後：

   ```powershell
   git fetch origin main
   git worktree add .worktrees/my-fix -b fix/my-fix origin/main
   Set-Location .worktrees/my-fix
   ```

4. 修改、驗證並提交該題需要的檔案。提交前用 `git diff --cached` 檢查內容。完成提交後，首次推送：

   ```powershell
   git push -u origin fix/my-fix
   ```

5. 在 GitHub 建立 PR，核對四個欄位：

   | GitHub 欄位                       | 要選的值                  |
   | --------------------------------- | ------------------------- |
   | base repository（接收修改的專案） | `ultralytics/ultralytics` |
   | base（接收修改的分支）            | `main`                    |
   | head repository（提供修改的專案） | `Echoslayer/ultralytics`  |
   | compare（提供修改的分支）         | `fix/my-fix`              |

直接從最新 `upstream/main` 建立功能分支，技術上也可行；但未同步的個人副本會讓比較畫面混入官方提交。本書採用先同步 fork、再從 `origin/main` 建立工作樹的順序，方便追蹤。

後續修正同一筆 PR，繼續推送原功能分支。完成本機提交後，先執行 `git pull --rebase`，再執行 `git push`；若有衝突，先解決。不要強制推送，也不要推到 `main`。

## 用覆蓋率找線索，再決定是否補測試

本地 CI 設定已使用 Codecov，入口是 [Ultralytics 覆蓋率報告](https://app.codecov.io/gh/ultralytics/ultralytics)。查看時先核對分支與提交版本，再找目標檔案未執行的行。此次無法讀取儀表板內容，因此不列目前百分比。

一般測試使用 `pytest --cov=ultralytics/ --cov-report=xml tests/ --export-env base` 產生報告，再由 CI 上傳。工作流程也為基準測試與 GPU 測試設定上傳步驟。個人副本的一般測試不會透過這個步驟上傳，因為它限定在官方專案執行。

覆蓋率表示程式曾被執行，不保證測試有檢查正確結果。`pyproject.toml` 還排除了 `ultralytics/utils/callbacks/*`，因此報告不是整個套件毫無排除的統計。以上依本地 `.github/workflows/ci.yml` 與 `pyproject.toml` 查核。

準備新增測試時，先找能重現的實際問題，再檢查既有測試是否漏掉高風險路徑。依本地規範，只有這類缺口才補最少的回歸測試（確認同一錯誤不會再次出現的測試）。不要只為提高百分比而新增大量模擬設備或平台的測試。

本機操作見下方流程。單一測試產生的覆蓋率只代表該次執行，不能直接與官方多個 CI 工作合併的報告比較。

### PR 上的 Codecov 留言：先看檢查狀態，再決定是否補測試

送出 PR 後，codecov bot 可能留言「Patch coverage is 0%」，並標出缺少覆蓋的行數。這則留言只是報告，判斷時依序看：

1. **`codecov/patch` 檢查是 pass 還是 fail。** pass 就不會擋合併。
2. **其他 Tests 是否還在跑。** 各 CI 工作陸續上傳覆蓋率，第一則留言的數字可能還會變。
3. **未覆蓋的行原本是否就沒有測試。** 若改動加在一段既有程式也沒被執行到的區塊，就不是這次漏的。
4. **是否屬於高風險缺口。** 不是的話不補；維護者要求時，再補最小的回歸測試。

不必回覆 codecov bot。實例見下方 #26949。

<a id="local-tests"></a>

## 在 Windows 本機跑測試：先跑一項，再擴大範圍

**使用獨立 Python 環境與測試目錄，先確認一項測試能執行。** 以下以 PowerShell、uv 和 CPU 測試為例，適合先驗證一般程式行為。GPU 問題仍須在相符設備與環境驗證。

所有步驟在同一個 PowerShell 視窗依序執行。命令失敗就先處理原因，不要直接跳到下一步。本節的環境建立、隔離設定、測試收集與單一圖片測試已在本機驗證；完整測試集尚未執行。

### 1. 指定正式修正的工作樹，建立 Python 環境

先依前面的 PR 流程建立工作樹。將下方路徑換成自己的修正目錄，不要指向主 checkout 或研究書分支。

```powershell
$repo = (Resolve-Path 'D:\tools\ultralytics\.worktrees\my-fix').Path
Set-Location $repo
git status --short
git rev-parse HEAD
uv --version
uv venv --python 3.13 .venv
$python = Join-Path $repo '.venv\Scripts\python.exe'
uv pip install --python $python -e '.[dev]' ruff --torch-backend cpu
```

這裡選 Python 3.13，對齊研究版本的主要 CI 測試版本，不表示其他支援版本不重要。若 `.venv` 已存在，先確認它是這次工作的環境，再跳過建立步驟。安裝需要網路與磁碟空間。

`-e` 表示直接使用工作樹中的程式，修改後不用重新安裝。`[dev]` 安裝 pytest（Python 測試工具）與覆蓋率工具；Ruff 是額外安裝的格式與程式檢查工具。命令直接指定環境內的 Python，不必執行 `Activate.ps1`。

### 2. 隔離設定、模型權重與測試輸出

測試結束時，`tests/conftest.py` 會清理：

- 目前工作目錄的 `bus.jpg`、`yolo26n.onnx`、`yolo26n.torchscript`。
- 權重目錄及子目錄中的 `*.onnx`、`*.torchscript`。
- 權重目錄及子目錄中的 `*.mlpackage`、`*_openvino_model` 資料夾。

即使只跑單一測試，也會執行這段清理。請先建立全新的暫存目錄，並讓 Ultralytics 使用獨立設定：

```powershell
$testRoot = Join-Path $env:TEMP ('ultralytics-test-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $testRoot | Out-Null
$env:YOLO_CONFIG_DIR = Join-Path $testRoot 'config'
$env:YOLO_AUTOINSTALL = 'false'
$env:COVERAGE_FILE = Join-Path $testRoot '.coverage'
Set-Location $testRoot
@'
import sys
from pathlib import Path
from ultralytics import settings

p = Path(sys.argv[1])
settings.update(weights_dir=str(p / 'weights'), datasets_dir=str(p / 'datasets'), runs_dir=str(p / 'runs'))
'@ | & $python - $testRoot
& $python -c 'import ultralytics; from ultralytics.utils import WEIGHTS_DIR, DATASETS_DIR, RUNS_DIR; print(ultralytics.__file__); print(WEIGHTS_DIR); print(DATASETS_DIR); print(RUNS_DIR)'
```

最後一個命令應顯示：套件來自 `$repo`，三個資料目錄都在 `$testRoot` 下。若不符，先停止並修正路徑。設定更新與路徑檢查分成兩個 Python 程序，讓第二個程序重新載入設定。

`YOLO_AUTOINSTALL=false` 禁止測試途中自動補裝套件，不會禁止下載模型或資料集。第一次執行仍可能從網路取得測試資源。這些環境變數只設定在目前視窗，完成後關閉視窗即可；不會改動原本的個人 Ultralytics 設定。

### 3. 先確認測試清單，再跑單一模型的圖片測試

先收集測試名稱，不執行測試本體。收集仍會匯入程式並執行測試階段的設定與清理，因此也要在上述隔離目錄執行。

```powershell
& $python -m pytest -c "$repo\pyproject.toml" "$repo\tests\test_python.py" --collect-only -q
& $python -m pytest -c "$repo\pyproject.toml" "$repo\tests\test_python.py::test_predict_img[yolo26n.pt]" -v
```

方括號指定參數化測試的一個模型。如果只寫 `test_predict_img`，pytest 會測試該函式列出的多個模型。正式修正時，請從收集結果選擇與修改有關的測試，不要把圖片測試通過當成所有功能都通過。

### 4. 為同一項測試產生覆蓋率報告

```powershell
& $python -m pytest -c "$repo\pyproject.toml" "$repo\tests\test_python.py::test_predict_img[yolo26n.pt]" --cov=ultralytics --cov-config="$repo\pyproject.toml" --cov-report=term-missing --cov-report=html:htmlcov --cov-report=xml:coverage.xml -v
Start-Process (Join-Path $testRoot 'htmlcov\index.html')
```

終端機列出未執行的行，`htmlcov/index.html` 提供逐檔網頁報告，`coverage.xml` 可交給其他報告工具。報告都留在 `$testRoot`。此處用套件名稱 `--cov=ultralytics`，因為目前目錄不是原始碼根目錄；`--cov-config` 則明確指定專案的覆蓋率設定。

### 5. 視修改範圍，擴大到檔案或一般測試集

只需要跑同一個檔案時：

```powershell
& $python -m pytest -c "$repo\pyproject.toml" "$repo\tests\test_python.py" -v
```

準備跑一般測試集前，補裝匯出與 solutions 所需套件。以下依研究版本 CI 的 CPU 安裝方式整理，需要 Git 才能安裝 CLIP：

```powershell
uv pip install --python $python -e "${repo}[dev,export-base,export-openvino,solutions]" aiohttp 'git+https://github.com/ultralytics/CLIP.git' --torch-backend cpu
& $python -m pytest -c "$repo\pyproject.toml" "$repo\tests" --export-env base --cov=ultralytics --cov-config="$repo\pyproject.toml" --cov-report=term-missing --cov-report=html:htmlcov --cov-report=xml:coverage.xml
```

本機先使用單一程序，方便定位錯誤並控制記憶體用量。需要加速且資源足夠時，再加入 `-n 2 --dist=loadfile`；CI 常用的 `-n auto` 會依可用 CPU 啟動多個工作程序，不一定適合你的電腦。

| 想驗證的範圍 | 做法與限制                                                                                               |
| ------------ | -------------------------------------------------------------------------------------------------------- |
| 預設一般測試 | 不含標記為 `slow` 的測試；通過不代表慢速測試也通過                                                       |
| 慢速測試     | 在選定測試命令加入 `--slow`；執行時間與資源需求可能增加                                                  |
| 特定匯出格式 | 先查 `engine/exporter.py` 的 `EXPORT_ENVS`，安裝對應環境，再選 `tests/test_exports.py` 與 `--export-env` |
| NVIDIA GPU   | 另建相符的 CUDA／PyTorch 環境，再跑 `tests/test_cuda.py`；上述 CPU 環境不能驗證 CUDA 行為                |

`--export-env base` 只篩選匯出測試，不會安裝套件，也不會取消平台或設備限制。移除這個參數仍不代表所有匯出格式都能執行。pytest 設定還啟用文件範例測試；不要把目標隨意改成 `ultralytics/`，那會多跑 CI 一般測試工作未涵蓋的程式內範例。

### 6. 記錄結果，先分清楚失敗原因

| 看到的結果                 | 下一步                                                           |
| -------------------------- | ---------------------------------------------------------------- |
| `passed`                   | 記下命令、版本與通過範圍，再檢查修改是否還影響其他功能           |
| `skipped` 或沒有收集到測試 | 讀取原因；需要時加 `-rs` 查看跳過原因，不要記成驗證成功          |
| 缺少套件或下載失敗         | 先處理環境與網路，不要直接判定為程式錯誤                         |
| 測試失敗                   | 保留完整錯誤，用相同環境比較修改前後；只在修改後失敗才是回歸線索 |
| 多程序執行失敗             | 移除 `-n`，以單一程序重跑失敗項目，確認是否與資源或檔案競爭有關  |

在 PR 寫下基準與修正後的提交編號、Python／PyTorch 版本、作業系統、CPU 或 GPU、完整命令、通過與跳過項目，以及未驗證範圍。若新增匯出測試，沿用既有 `isolated_model` 測試資源，避免平行測試覆寫同名匯出檔。

下一步：先完成第 1 至 3 步，再換成你準備修改的模組所對應的測試。本節依本地 `tests/conftest.py`、`tests/test_python.py`、`pyproject.toml`、`ultralytics/utils/__init__.py` 與 `.github/workflows/ci.yml` 整理。

### 本機實測紀錄（2026-10-28）

本次使用 uv 在研究工作樹建立 `.venv-local-test`，以可編輯模式安裝目前程式，驗證上述操作流程。正式修正仍應另開乾淨工作樹。

| 項目       | 實測結果                                                                                        |
| ---------- | ----------------------------------------------------------------------------------------------- |
| 原始碼版本 | `9894f819ba16d9962e140d9ce84bba3441da1173`，Ultralytics `8.4.191`；模型程式未修改               |
| 環境       | Windows、Python `3.13.14`、PyTorch `2.14.1+cpu`、pytest `9.2.0`                                 |
| 環境管理   | `uv venv --python 3.13 .venv-local-test`；`uv pip install` 安裝 `[dev]`、Ruff 與 CPU 版 PyTorch |
| 路徑檢查   | 套件來自研究工作樹；設定、權重、資料與輸出都使用專用暫存目錄                                    |
| 收集測試   | `test_python.py` 成功收集 180 個測試；不代表這 180 個都已執行                                   |
| 執行測試   | `test_python.py::test_predict_img[yolo26n.pt]`：`1 passed`，整次執行 34.42 秒                   |
| 覆蓋率     | 單次套件行覆蓋率約 16%；已產生 `htmlcov/index.html` 與 `coverage.xml`，不能當成完整測試集的結果 |

本次環境保留在 `D:\tools\ultralytics\.worktrees\contribution-research\.venv-local-test`。報告與記錄保留在 `C:\Users\edisonhsieh\AppData\Local\Temp\ultralytics-test-33e4a640e1064ee1b6e2c31c405d7f29`，包括 `collect.log` 與 `test-coverage.log`。暫存目錄可能被系統清除，需要長期保存時請複製整個報告目錄。

若要沿用環境重跑，先將第 1 步的 `$repo` 設為研究工作樹，並將 `$python` 設為 `Join-Path $repo '.venv-local-test\Scripts\python.exe'`，跳過建立與安裝環境，再從第 2 步建立新的隔離測試目錄。也可以用 `uv pip list --python $python` 查看這個環境的套件。

安裝初次受到執行沙箱的連線限制，允許連線後完成。另一次路徑檢查在安裝尚未完成時過早啟動，出現 PyTorch 匯入錯誤；等待 uv 成功結束後，重跑通過。完整測試集、慢速測試、匯出與 GPU 測試尚未驗證。

## PR 說清楚問題、結果與未驗證範圍

2026-10-29 查核的[官方共用 PR 模板](https://github.com/ultralytics/.github/blob/main/PULL_REQUEST_TEMPLATE.md)沒有強制正文標題或 `docs:` 等標題前綴。它要求先查重、清楚說明修改、連結相關議題並處理 CLA。[貢獻指南](https://github.com/ultralytics/ultralytics/blob/main/CONTRIBUTING.md)則要求清楚的標題、目的與範圍。

小型文件修改可用 `Summary` 與 `Validation` 兩段，這是本書建議，不是官方格式。先指出讀者會誤解什麼，再說明修正及實際驗證。Ultralytics Actions 會另外產生摘要，不必仿寫其格式。研究提案保留中英文對照，正式 PR 只提交英文；依 ISO 24495-1 編寫，不必在 PR 宣告採用 ISO。

PR 描述至少回答四個問題：

- 哪種輸入與環境會出錯？
- 修改後的行為是什麼？
- 跑了哪些驗證，結果如何？
- 哪些平台或功能還沒驗證？

附上原議題連結。只寫「提高穩定性」不足以讓審查者判斷是否解決問題。

請閱讀每一項自動審查建議，採用或說明不適用的原因。CI（自動建置與測試流程）通過，也不能取代完整的程式審查。[自動審查說明](https://github.com/ultralytics/ultralytics/blob/main/CONTRIBUTING.md)

合併前需處理 CLA（貢獻者授權協議）。請本人閱讀文件並依自動工具指示簽署，不能由代理代簽。溝通時遵守[社群行為準則](https://docs.ultralytics.com/help/code-of-conduct/)，也要區分推測與已確認根因。

### CLA 失敗時，先讀 bot 訊息

`CLA / CLA` 失敗不一定是程式或 Actions 設定問題。若 bot 列出作者尚未簽署，作者應先閱讀 [CLA](https://docs.ultralytics.com/help/CLA)，同意後在 PR 的 **Conversation → Add a comment** 貼上指定文字，按 **Comment**：

```text
I have read the CLA Document and I sign the CLA
```

這是留言，不是修改 PR 描述。之後查看 bot 與 CLA 檢查是否更新；沒有必要只為這件事修改程式或重新 push。

### AI 輔助目前沒有必填聲明欄位

2026-10-29 查閱的貢獻指南、共用 PR 模板與 [AGENTS.md](https://github.com/ultralytics/ultralytics/blob/main/AGENTS.md)沒有找到強制揭露 AI 輔助的要求。審查規範反對沒有價值的 AI 生成內容，不能解讀成全面禁止 AI 工具。若維護者詢問，應如實說明。

同日抽查 `gh pr list --state merged --limit 30` 回傳的 30 個近期已合併 PR，搜尋正文與作者主討論留言並排除機器人摘要，找到 1 個明確聲明：[PR #26912](https://github.com/ultralytics/ultralytics/pull/26912) 提到 Claude 與 GPT-6 Astra 輔助，已於 2026-10-27 合併。其餘 29 個沒有找到明確聲明，不代表沒有使用 AI。這不是按合併時間嚴格排序的全量調查，未查逐行留言、commit 訊息或歷史編輯版本，也不能推論聲明影響合併率。

**本書做法（2026-10-30 起）：PR 與 commit 預設都不填 AI 輔助聲明。** PR 正文不加 `🤖 Generated with Claude Code` 標語，也不加「AI-assisted…」說明句；`proposals/*/PR.md` 的草稿也一樣。commit 訊息不加 `Co-Authored-By: Claude …`。維護者詢問時如實回答。[PR #26949](https://github.com/ultralytics/ultralytics/pull/26949) 是在這項決定之前送出的：正文仍保留一句說明，提交 `00e6e8030` 也帶有 `Co-Authored-By`。已推送的提交不改寫，因為規範禁止 force push。

## 實例：從 T01／T05 到文件 PR #26935

T01 觀察到設定 `weights_dir` 後，裸模型檔名的缺檔下載仍進入工作目錄。T05 再驗證查找順序，將問題收斂成文件澄清。最終 [PR #26935](https://github.com/ultralytics/ultralytics/pull/26935) 只在 Settings 頁新增 10 行英文說明與範例，沒有改變下載程式。

| 階段     | 實際處理與證據                                                                                                             |
| -------- | -------------------------------------------------------------------------------------------------------------------------- |
| 查重     | 讀 #18435、#17513 的解答及未合併 PR #24150；確認文件澄清與改下載行為是不同範圍。關閉原因見[第六章](ticket-requirements.md) |
| 基準     | 官方 main `922563eab42b778445e55a2edbabb6974eed8e4b`；個人副本原落後 1 筆且無獨有提交，後來快轉同步                        |
| 工作樹   | `.worktrees/weights-dir-docs`，功能分支 `docs/clarify-weights-dir`；研究書留在 `contribution-research`                     |
| 本地驗證 | 直接匯入該工作樹的程式碼，在 Windows／CPU 驗證工作目錄優先、weights_dir 查找、裸檔名缺檔下載與完整路徑下載，四種均通過     |
| 文件檢查 | Prettier 3.9.9、`git diff --check`、`python docs/build_docs.py` 完整嚴格建置通過；Windows 建置使用 `PYTHONUTF8=1`          |
| 提交     | `7d58cf0fa5b6616d1758c4058d0e213d2b9cc056`，只包含 Settings 文件；英文 PR 敘述附驗證結果                                   |
| CLA      | 首次因未簽署失敗；作者本人留言後，bot 確認所有作者已簽署，檢查成功                                                         |

**狀態快照：2026-10-29，PR 仍開啟，尚未合併。** 上述提交的 20 個檢查中，14 個成功、6 個跳過，沒有執行中或失敗項目。UltralyticsAssistant 已核可並表示沒有發現問題；這是自動審查，不等於人工核可或保證合併。[PR 檢查](https://github.com/ultralytics/ultralytics/pull/26935/checks)、[CLA 確認](https://github.com/ultralytics/ultralytics/pull/26935#issuecomment-6486715262)

這次同步曾被錯誤的認證帳號擋住。`gh auth status` 顯示環境變數 `GITHUB_TOKEN` 優先於儲存的登入；`gh auth switch` 因此無法直接切換。僅在執行程序中移除該覆蓋，再切換至有權限的 Echoslayer，才完成同步。遇到 403，先查目前帳號與權限，不要公開 token，也不要把認證問題當成 Git 分支分歧。

此案例的模型實測限 Windows／CPU，沒有驗證其他格式或 URL；暫存驗證腳本與日誌可能被系統清除。遠端跳過的 GPU 等檢查不算成功測試。之後若 bot 或維護者更新提交，應重新確認最新差異與檢查結果。

## 實例：從 issue #26943 到程式 PR #26949

這個案例先開 issue，等維護者選定方向後才送 PR，因為修改會碰到安全載入的允許清單。維護者 Y-T-G 回覆「可以開 PR 加進允許清單」，也就是提案中的 A 案。最終 [PR #26949](https://github.com/ultralytics/ultralytics/pull/26949) 只在 `_SafeLoad.loading()` 原本的 torchvision 轉換群組加入 `ToPILImage`、`ClassifyLetterBox` 和 `np.asarray`。提案與 PR 草稿見 [safe-load-custom-transforms](../../../proposals/safe-load-custom-transforms/README.md)。

| 階段     | 實際處理與證據                                                                                                                   |
| -------- | -------------------------------------------------------------------------------------------------------------------------------- |
| 方向     | issue #26943 列出 A（擴充允許清單）與 C（改錯誤訊息）兩案；維護者選 A，因此不同時改錯誤訊息                                      |
| 基準     | 官方 main `80c34c050`；個人副本 `origin` 落後，改從上游 main 開分支                                                              |
| 工作樹   | `ultralytics/.worktree/safe-load-cls-transforms`，功能分支 `safe-load-cls-transforms`                                            |
| 範圍     | 只改 `ultralytics/nn/tasks.py`，送出時 +14/−1，維護者縮成兩行後以 +4/−1 合併；只放行實際存進 checkpoint 的驗證轉換，文件中的訓練增強不存進模型，所以不放行       |
| 本地驗證 | macOS／CPU、Python 3.12、torch 2.15.0：issue 的 MRE 修改前失敗、修改後可安全載入並推論；`-k "restricted or remaps_cls"` 4 個通過 |
| 提交     | `00e6e8030`，PR 正文沿用 #26935 的 Summary／Validation 結構                                                                      |

**狀態快照：2026-10-30，PR 仍開啟，尚未合併。** UltralyticsAssistant 已自動核可；19 個檢查中 5 個成功、6 個跳過、8 個仍在執行。自動核可不等於人工核可或保證合併。

這次遇到三個值得記下的問題：

- **訓練輸出寫進其他專案。** 沒有指定 `project=` 時，訓練結果寫到 Ultralytics 設定中的 `runs_dir`，這次落在另一個專案的目錄下。跑重現腳本時，應指定 `project=` 到暫存目錄。
- **改寫 PR 正文會蓋掉 bot 摘要。** Ultralytics Actions 會把「🛠️ PR Summary」寫進 PR 正文。用 `gh pr edit --body-file` 整份覆蓋前，先抓下線上正文再修改。若已蓋掉，可從 GraphQL 的 `userContentEdits` 找回 bot 的版本。
- **再次遇到 403。** 預設的 git 憑證屬於另一個帳號。這次只在單次指令中改用 Echoslayer 的憑證（`gh auth token --user Echoslayer`），沒有切換全域登入。

**Codecov 報告 0%，決定不補測試。** codecov bot 第一則留言回報 `ultralytics/nn/tasks.py` 有 2 行未覆蓋，維護者縮短程式、CI 跑完後，留言最終是 3 行未覆蓋，正好印證上面第 2 點：數字會變。`codecov/patch` 檢查始終是 pass。新增的三項加在 torchvision 轉換區塊，這段只在 checkpoint 存有 torchvision 轉換、且開啟安全載入時才執行，原本的 5 個轉換同樣沒有測試跑到。要覆蓋它，得在 CI 訓練分類模型，或手工做一個含轉換的 checkpoint；對只多放行三項的修改來說，風險低、測試比修正還長，所以不補。若維護者要求，再加一個不需訓練的最小測試：用 `torch.save` 存下 `T.Compose([np.asarray, ClassifyLetterBox(64), T.ToPILImage()])`，再以 `torch_safe_load(..., safe_only=True)` 載入，約 6 行。

此案例沒有在 Windows 或 Linux 上驗證。作者先前的實測都在 Windows，送出後可補跑一次。

下一步：選定一種貢獻，再用[第二章的檔案對照表](codebase-map.md)找出負責模組。
