# T15 提案：修正不會結束的 screen 與 webcam 範例

狀態：2026-11-01 已在官方 main `58876de55`（8.4.194）完成修改與本地驗證。工作樹 `ultralytics/.worktree/screen-source-docs`，分支 `docs/screen-source-stream`，commit `dd7daad40`、`3f1e876d7`，已送出 [PR #26979](https://github.com/ultralytics/ultralytics/pull/26979)，等待審查。改 `docs/en/modes/predict.md` 與 `docs/en/usage/python.md`（+9/−6），不改程式碼。PR 草稿見 [PR.md](PR.md)。

## 為什麼值得做

文件把 `"screen"` 寫成拍一張截圖，範例是 `results = model(source)`。實際上 `LoadScreenshots` 沒有結束條件，`stream=False` 又要收完整個來源才回傳，所以這行永遠不會返回，也沒有錯誤。程式只印通用的 `stream=True` 記憶體警告，讀者看不出來源不會結束。

- 範例原樣跑 110 秒仍未返回（[`screen.log`](assets/screen.log)）；另一次 41 秒已到 800 幀，60 秒時被強制結束（[`screen_frames.log`](assets/screen_frames.log)）。
- **記憶體會持續增加。** 每個 `Results` 都保留 `orig_img`，`stream=False` 全部留在 list 裡。在 1470×956 螢幕上，範例跑 63 秒時實體用量到 6.9 GB，約每秒 110 MB（[`mem.log`](assets/mem.log)）。依這個速度，16 GB 的機器大約幾分鐘內會耗盡；這是推算，沒有實際跑到 OOM。
- `usage/python.md:138` 的 `model.predict(source="0")` 是同一個問題。用假的 `cv2.VideoCapture` 餵 640×480 影格，真正的 `LoadStreams` 與 predictor 跑 64 秒仍未返回，用量到 1.8 GB；只有鏡頭自己停止時才會返回。
- 這段範例至少從 2024 年就是這樣。
- 2026-10-31 搜尋 issue 與 open PR，沒有找到相同回報或處理中的修改。
- 證據：[T15 紀錄](../../research/tutorial-audit/records/T15.md)

## 最小修改範圍

1. 來源表：列標上 ✅，Notes 改成 “Capture the screen continuously until you stop.”
2. screenshot 分頁的說明改成來源會持續擷取。
3. 範例改用 `stream=True` 的迴圈，取到第一幀就 `break`。
4. `usage/python.md:138` 改成同樣的 `stream=True` 迴圈，取到第一幀就 `break`。

這件事不需要先開 issue：只改文件，問題可以直接重現。

## 驗證

環境：macOS（Apple Silicon）、Python 3.13.12、torch 2.15.0、CPU。

- [`verify_screen_doc.py`](assets/verify_screen_doc.py) 從修改後的頁面取出範例原樣執行：3.7 秒結束，exit 0，有印出 boxes，沒有記憶體警告（[`verify_screen_doc.log`](assets/verify_screen_doc.log)）。
- [`verify_webcam_line.py`](assets/verify_webcam_line.py) 從修改後的頁面取出 webcam 寫法，用假鏡頭原樣執行：開啟的來源是 `0`，讀到一幀就停止（[`verify_webcam_line.log`](assets/verify_webcam_line.log)）。
- Prettier 3.9.9（`--tab-width 4 --print-width 120`）與 `git diff --check` 通過。
- `python docs/build_docs.py` 完整嚴格建置通過（No issues found，[`build-docs.log`](assets/build-docs.log)），工作樹只留這兩個檔案的修改。
- 沒有用實體鏡頭測試，也沒有在 Windows、Linux 或無顯示器環境測試。

## 不在範圍內

- 讓 `"screen"` 只截一張，或為它加上結束條件：屬於程式行為變更，要另外討論。
- `Ctrl+C` 之後的行為與 CLI 的 `source=screen`：沒有測。

---

# T15 proposal: fix the screen and webcam examples that never end

Status: implemented and locally validated on official main `58876de55` (8.4.194) on 2026-11-01. Worktree `ultralytics/.worktree/screen-source-docs`, branch `docs/screen-source-stream`, commits `dd7daad40` and `3f1e876d7`, submitted as [PR #26979](https://github.com/ultralytics/ultralytics/pull/26979); awaiting review. Changes `docs/en/modes/predict.md` and `docs/en/usage/python.md` (+9/−6), no code changes. PR draft: [PR.md](PR.md).

## Why

The docs describe `"screen"` as taking one screenshot, and the example is `results = model(source)`. In fact `LoadScreenshots` has no end condition and `stream=False` collects the whole source before returning, so that line never returns and raises no error. The only output is the generic `stream=True` memory warning, which does not tell readers that the source never ends.

- The example as written had not returned after 110 s ([`screen.log`](assets/screen.log)); another run reached 800 frames at 41 s and was killed at 60 s ([`screen_frames.log`](assets/screen_frames.log)).
- **Memory keeps growing.** Every `Results` keeps `orig_img`, and `stream=False` holds them all in the list. On a 1470×956 screen the example reached 6.9 GB of physical footprint at 63 s, about 110 MB/s ([`mem.log`](assets/mem.log)). At that rate a 16 GB machine runs out within minutes; this is a projection, not an observed OOM.
- `model.predict(source="0")` at `usage/python.md:138` has the same problem. With a fake `cv2.VideoCapture` feeding 640×480 frames, the real `LoadStreams` and predictor had not returned after 64 s and reached 1.8 GB; the call returns only when the camera itself stops.
- The example has read this way since at least 2024.
- A search of issues and open PRs on 2026-10-31 found no matching report or work in progress.
- Evidence: [T15 record](../../research/tutorial-audit/records/T15.md)

## Minimal change

1. Source table: mark the row ✅ and change Notes to "Capture the screen continuously until you stop."
2. Change the screenshot tab's description to say the source keeps capturing.
3. Change the example to a `stream=True` loop that breaks after the first frame.
4. Change `usage/python.md:138` to the same `stream=True` loop, breaking after the first frame.

No issue is needed first: this is docs only and directly reproducible.

## Validation

Environment: macOS (Apple Silicon), Python 3.13.12, torch 2.15.0, CPU.

- [`verify_screen_doc.py`](assets/verify_screen_doc.py) takes the example from the changed page and runs it as written: finished in 3.7 s, exit 0, boxes printed, no memory warning ([`verify_screen_doc.log`](assets/verify_screen_doc.log)).
- [`verify_webcam_line.py`](assets/verify_webcam_line.py) takes the webcam lines from the changed page and runs them on a fake camera: it opens source `0` and stops after one frame ([`verify_webcam_line.log`](assets/verify_webcam_line.log)).
- Prettier 3.9.9 (`--tab-width 4 --print-width 120`) and `git diff --check` pass.
- `python docs/build_docs.py`: full strict build passed (no issues found, [`build-docs.log`](assets/build-docs.log)); only these two files remain changed in the working tree.
- Not tested with a real camera, on Windows or Linux, or without a display.

## Out of scope

- Making `"screen"` capture once or adding an end condition: a code behavior change that needs separate discussion.
- Behavior after `Ctrl+C` and the CLI `source=screen`: not tested.

這些是研究草稿，不代表已取得維護者同意。/ This is a research draft, not evidence of maintainer approval.
