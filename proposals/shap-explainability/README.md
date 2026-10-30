# 評估：替 YOLO 內建 SHAP 解釋

狀態：2026-10-30 評估紀錄。結論是**不建議直接做成上游 PR**。沒有建立分支，也沒有開 issue。

## 結論先講

上游目前沒有 SHAP，但已經有梯度式熱圖（LayerCAM）。新增 SHAP 屬於功能 PR，門檻很高，維護者過去兩次都建議使用者在外部自己包裝。若仍想推動，**先開功能 issue 取得明確同意**；被拒就改做外部範例或套件。

## 上游現況（main `0056e6ce1`，8.4.193）

- 程式碼與文件都搜不到 `shap`、`shapley`、`captum`。
- 已有可解釋性功能：`visualize=True` 會在 predict 時存下 LayerCAM 類別激活熱圖。
  - 設定：`ultralytics/cfg/default.yaml` 的 `visualize`。
  - 實作：`ultralytics/utils/plotting.py` 的 `class_activation_map()`，以正梯度加權 head 輸入，各預測、各層級分別正規化後取最大值。
  - 限制：只支援 PyTorch 權重；`augment`、`embed`、tensor 輸入與匯出格式會略過並警告（`ultralytics/engine/predictor.py`）。
  - 來源：[PR #25548](https://github.com/ultralytics/ultralytics/pull/25548)，2026-07-30 合併，+140/−75，取代舊的特徵圖輸出。
- `val` 模式的 `visualize` 是畫 TP/FP/FN，不是熱圖。

## 上游對 SHAP 的態度

| 議題 | 結果 | 維護者回覆重點 |
| --- | --- | --- |
| [#13809](https://github.com/ultralytics/ultralytics/issues/13809) YOLOv8 分割 + SHAP（2024-06） | 無人回應後關閉（not planned） | 提供外部範例；使用者回報範例跑不起來，最後沒有後續 |
| [#23719](https://github.com/ultralytics/ultralytics/issues/23719) YOLO11 SHAP（2026-02） | 使用者自行解決後關閉 | 偵測模型輸出的框數量不固定，必須先定義固定的純量目標（例如「類別 k 的最高信心值」）再解釋 |

其他 Grad-CAM 提問（#2020、#14736、#23730、#23819）也都是使用問題，沒有功能 PR。以上是 2026-10-30 用 `gh search issues` 搜尋 `shap`、`shapley`、`explainability`、`grad-cam` 的結果。

## 為什麼不建議直接送 PR

依 `CONTRIBUTING.md`（Feature PRs）與 `AGENTS.md`（PR Review）：

1. **功能 PR 必須先有 issue，並取得維護者明確同意。**沒有 issue 直接送，很可能被關。
2. **淨新增超過 50 行、新增參數或新增依賴，都算高門檻例外。**SHAP 需要「挑出某個框、某個分數」的包裝、背景樣本與視覺化，很難壓在 50 行內。
3. **不能新增基礎依賴。**`shap` 只能在用到的地方以 `check_requirements("shap")` 延遲安裝。
4. **功能要擴充既有的負責模組。**最自然的位置是 `visualize` 與 `class_activation_map()`，不能另開一套平行的 explain 模組。審查者一定會問：LayerCAM 為什麼不夠？
5. **小眾、太慢的功能會被關。**SHAP 需要大量重複推論，對偵測模型來說很慢。
6. **不鼓勵第一次貢獻的人送功能 PR。**

## 如果還是要做：流程

1. 搜尋既有討論（上表），在功能 issue 中引用。
2. 寫英文功能 issue，說清楚**哪些情境 LayerCAM 做不到、只有 SHAP 才行**（例如需要可加性歸因、要做模型稽核），以及預計修改的最小範圍。
3. 等維護者明確同意。沒同意就停，改走下方的替代方案。
4. 同意後，依[第一章](../../research/contributing/docs/contribution-workflow.md)開乾淨的工作樹與分支，在既有負責模組上實作；Google-style docstring、`ruff format`、`ruff check`。
5. 送 PR，連回 issue，說明為什麼沒辦法再縮小。簽 CLA，等 Ultralytics Actions 的格式化提交與自動審查，`git pull --rebase` 後逐項處理。

## 替代方案（不受上游門檻限制）

- 在自己的 repo 用 `shap.GradientExplainer` 或 `captum` 包住 `model.model`，加一個輸出固定純量的包裝器（例如類別 k 的最高分數）。
- 想累積貢獻紀錄，先送小型錯誤修正或文件 PR，之後再提功能。

---

# Assessment: built-in SHAP explanations for YOLO

Status: assessment record, 2026-10-30. Conclusion: **do not open an upstream PR directly**. No branch or issue yet.

## Bottom line

Upstream has no SHAP, but it already ships gradient-based heatmaps (LayerCAM). SHAP would be a feature PR with a high bar, and maintainers have twice told users to wrap the model externally. To pursue it, **open a feature issue and get explicit approval first**; if declined, publish an external example or package instead.

## Upstream state (main `0056e6ce1`, 8.4.193)

- No `shap`, `shapley`, or `captum` anywhere in code or docs.
- Existing explainability: `visualize=True` saves LayerCAM class activation heatmaps during predict.
  - Setting: `visualize` in `ultralytics/cfg/default.yaml`.
  - Implementation: `class_activation_map()` in `ultralytics/utils/plotting.py`; weights head inputs by positive gradients, normalizes each prediction and level, then takes the maximum.
  - Limits: PyTorch weights only; `augment`, `embed`, tensor inputs, and exported formats are skipped with a warning (`ultralytics/engine/predictor.py`).
  - Origin: [PR #25548](https://github.com/ultralytics/ultralytics/pull/25548), merged 2026-07-30, +140/−75, replacing feature-map dumps.
- `visualize` in `val` plots TP/FP/FN, not heatmaps.

## Upstream stance on SHAP

| Issue | Outcome | Maintainer reply |
| --- | --- | --- |
| [#13809](https://github.com/ultralytics/ultralytics/issues/13809) YOLOv8 seg + SHAP (2024-06) | Closed as stale (not planned) | Gave an external example; the user reported it failed, no follow-up |
| [#23719](https://github.com/ultralytics/ultralytics/issues/23719) YOLO11 SHAP (2026-02) | Closed after the user solved it | Detection returns a variable number of boxes, so define a fixed scalar target (e.g. max confidence for class k) and explain that |

Other Grad-CAM questions (#2020, #14736, #23730, #23819) were usage questions with no feature PR. Searched with `gh search issues` for `shap`, `shapley`, `explainability`, and `grad-cam` on 2026-10-30.

## Why not a direct PR

Per `CONTRIBUTING.md` (Feature PRs) and `AGENTS.md` (PR Review):

1. **Feature PRs require a prior issue with explicit maintainer approval.**
2. **More than 50 net added code lines, new arguments, or new dependencies are high-barrier exceptions.** A box/score target wrapper, background samples, and plotting will hardly fit in 50 lines.
3. **No new base dependencies.** `shap` may only be installed lazily with `check_requirements("shap")` where used.
4. **Extend the existing owner.** That is `visualize` and `class_activation_map()`, not a parallel explain module. Reviewers will ask why LayerCAM is not enough.
5. **Niche or slow features get closed.** SHAP needs many forward passes and is slow on detectors.
6. **Feature PRs from first-time contributors are discouraged.**

## If pursuing it anyway

1. Search existing discussions (table above) and cite them in the issue.
2. Write an English feature issue stating **which cases LayerCAM cannot cover and SHAP can** (e.g. additive attributions, model audits) and the minimal planned change.
3. Wait for explicit approval. Without it, stop and use the alternatives below.
4. Once approved, follow [chapter 1](../../research/contributing/docs/contribution-workflow.md): clean worktree and branch, extend the existing owner, Google-style docstrings, `ruff format`, `ruff check`.
5. Open the PR linking the issue and justifying why it cannot be smaller. Sign the CLA, wait for the Ultralytics Actions format commit and automated review, `git pull --rebase`, and address every finding.

## Alternatives outside the upstream bar

- Wrap `model.model` with `shap.GradientExplainer` or `captum` in your own repo, adding a wrapper that returns a fixed scalar (e.g. the top score for class k).
- To build a track record, send small bug fixes or docs PRs first, then propose features.
