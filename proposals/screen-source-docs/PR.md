# PR 草稿：中英文版本 / Bilingual PR draft

中文版供閱讀與討論；提交上游時只複製英文標題與正文。2026-11-01 已在獨立 worktree 完成修改與本地驗證，送出 [PR #26979](https://github.com/ultralytics/ultralytics/pull/26979)。

實作位置：`ultralytics/.worktree/screen-source-docs`。分支：`docs/screen-source-stream`（已推到 Echoslayer fork）。基準：官方 main `58876de55`（8.4.194）。commit `dd7daad40`、`3f1e876d7`，修改 `docs/en/modes/predict.md` 與 `docs/en/usage/python.md`，+9/−6，沒有修改產品程式碼。驗證腳本與日誌見 [assets](assets/)。

## 中文閱讀版

### 建議標題

修正文件裡不會返回的 screen 與 webcam 範例

### 建議正文

#### 摘要

Predict 頁把 `"screen"` 寫成拍一張截圖，範例是 `results = model(source)`。但 `LoadScreenshots` 不會結束，而 `stream=False` 要收完整個來源才回傳，所以這行永遠不會返回。它一直在跑，沒有錯誤，只有一條通用的記憶體警告，而每一幀都留在 list 裡，所以用量會一直漲：我的 1470×956 螢幕跑 63 秒就到 6.9 GB。

`usage/python.md` 的 `model.predict(source="0")` 是同一件事，webcam 不關掉就不會返回。

我在來源表把 screen 那列標成 ✅，說明改成會持續擷取，範例改用 `stream=True` 並在第一幀後跳出迴圈；webcam 那行也改成同樣的 `stream=True` 迴圈。

只改文件，不改程式碼。

#### 驗證

- 在 main `58876de55`（macOS、CPU、Python 3.13.12、torch 2.15.0）跑原本的範例，110 秒後仍未返回；另一次 41 秒已處理 800 幀，60 秒時被我強制結束。
- 新範例照原樣跑，約 4 秒結束，exit 0，有印出 boxes。
- 我沒有用實體鏡頭。webcam 是用假的 `cv2.VideoCapture` 餵影格，走真正的 `LoadStreams` 和 predictor：舊寫法 64 秒未返回，用量到 1.8 GB；新寫法讀到一幀就停止。
- Prettier 3.9.9 與 `git diff --check` 通過，`python docs/build_docs.py` 建置沒有問題。
- 還沒在 Windows、Linux 或無顯示器的環境試過。

---

## English submission draft

Status: implemented and locally validated on 2026-11-01 in a separate worktree. Submitted as [PR #26979](https://github.com/ultralytics/ultralytics/pull/26979).

## Suggested title

```text
Fix the screen and webcam examples that never return
```

## Suggested body

```markdown
## Summary

The Predict page describes `"screen"` as taking a screenshot, and its example is `results = model(source)`. But `LoadScreenshots` never ends and `stream=False` collects the whole source before returning, so that line never returns. It just keeps running with no error, the only hint is the generic memory warning, and every frame stays in the list, so memory keeps climbing: 6.9 GB after 63 s on my 1470×956 screen.

`model.predict(source="0")` in `usage/python.md` has the same problem: it won't return until the webcam stops.

I've marked the screen row ✅ in the source table, reworded it to say the source keeps capturing, and changed the example to use `stream=True` and leave the loop after the first frame. The webcam line now uses the same `stream=True` loop.

Docs only, no code changes.

## Validation

- Ran the old example on main `58876de55` (macOS, CPU, Python 3.13.12, torch 2.15.0): it hadn't returned after 110 s, and another run had processed 800 frames at 41 s when I killed it at 60 s.
- Ran the new example as written: it finishes in about 4 s with exit 0 and prints the boxes.
- I didn't use a real camera. For the webcam I fed frames through a fake `cv2.VideoCapture` into the real `LoadStreams` and predictor: the old line hadn't returned after 64 s and had reached 1.8 GB; the new loop reads a frame and stops right away.
- Prettier 3.9.9 and `git diff --check` pass, and `python docs/build_docs.py` builds cleanly.
- I haven't tried Windows, Linux, or a machine without a display.
```

The section headings above are a suggested structure, not mandatory Ultralytics fields.

上述章節是建議結構，不是 Ultralytics 必填欄位。
