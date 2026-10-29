# PR 草稿：中英文版本 / Bilingual PR draft

中文版供閱讀與討論；提交上游時只複製英文標題與正文。2026-10-30 已在獨立 worktree 完成修改與本地驗證，送出 [PR #26949](https://github.com/ultralytics/ultralytics/pull/26949)，對應 issue [#26943](https://github.com/ultralytics/ultralytics/issues/26943)。

實作位置：`/Users/wizard/Desktop/MacCode/ultralytics/.worktree/safe-load-cls-transforms`。分支：`safe-load-cls-transforms`。基準：官方 main `80c34c050`。只修改 `ultralytics/nn/tasks.py` 一個檔案，淨增約 12 行，沒有新增測試。

## 中文閱讀版

### 建議標題

讓安全載入接受文件自訂分類轉換訓練出的模型

### 建議正文

#### 摘要

讓安全載入模式能載入照文件[自訂轉換](https://docs.ultralytics.com/tasks/classify/#custom-transforms)範例訓練出的分類模型。

分類 trainer 會把驗證轉換存進模型。文件範例用 `T.Compose([np.asarray, ClassifyLetterBox(imgsz), T.ToPILImage()])` 做 letterbox，所以 `ULTRALYTICS_SAFE_LOAD=1` 和 `torch_safe_load(..., safe_only=True)` 會拒絕訓練出的 `best.pt`。

依 issue 中維護者的建議，在 `_SafeLoad.loading()` 原本的 torchvision 轉換群組加入 `ToPILImage`、`ClassifyLetterBox` 和 `np.asarray`。只有序列化了 torchvision 轉換的 checkpoint 才會註冊這三項。文件中的訓練增強不會存進模型，所以不必放行。

這三項在 unpickle 時都不會造成危害：`np.asarray` 只會轉換同樣在允許清單內的參數；兩個類別透過 `__dict__` 還原，不會呼叫 `__call__`。

Fixes #26943

#### 驗證

- 以官方 main `80c34c050` 在 macOS／CPU、Python 3.12、torch 2.15.0、torchvision 0.29.2、numpy 2.5.4 跑 issue 的 MRE。修改前，`safe_only=True` 拋出相同的 `TypeError`；修改後可以載入，`YOLO(best.pt)` 也能用存下的轉換推論。
- `pytest tests/test_python.py -k "restricted or remaps_cls"`：4 個通過。
- `ruff format --check` 和 `ruff check` 通過。
- 沒有在 Windows 或 Linux 上測試。

---

## English submission draft

Status: implemented and locally validated on 2026-10-30 in a separate worktree. Submitted as [PR #26949](https://github.com/ultralytics/ultralytics/pull/26949) for issue [#26943](https://github.com/ultralytics/ultralytics/issues/26943).

Worktree: `/Users/wizard/Desktop/MacCode/ultralytics/.worktree/safe-load-cls-transforms`. Branch: `safe-load-cls-transforms`. Base: upstream main `80c34c050`. The change touches only `ultralytics/nn/tasks.py`, adds about 12 net lines, and adds no tests.

## Suggested title

```text
Allow docs custom classify transforms under safe load
```

## Suggested body

```markdown
## Summary

Let restricted loading accept classifiers trained with the documented
[custom transforms](https://docs.ultralytics.com/tasks/classify/#custom-transforms).

The classification trainer stores the validation transforms on the model.
The docs example letterboxes with
`T.Compose([np.asarray, ClassifyLetterBox(imgsz), T.ToPILImage()])`, so
`ULTRALYTICS_SAFE_LOAD=1` and `torch_safe_load(..., safe_only=True)` reject
the resulting `best.pt`.

Add `ToPILImage`, `ClassifyLetterBox`, and `np.asarray` to the existing
torchvision transforms group in `_SafeLoad.loading()`, as suggested in the
issue. Only checkpoints that serialize torchvision transforms register them.
The docs' training augmentations are never saved, so they need no entries.

None of the three can do anything harmful at unpickle time: `np.asarray`
only converts allow-listed arguments, and the two classes are restored
through `__dict__` without calling `__call__`.

Fixes #26943

## Validation

- Ran the issue's MRE against upstream main `80c34c050` on macOS/CPU,
  Python 3.12, torch 2.15.0, torchvision 0.29.2, numpy 2.5.4. Before the
  fix, `safe_only=True` raised the same `TypeError`. After the fix it loads,
  and `YOLO(best.pt)` predicts through the saved transforms.
- `pytest tests/test_python.py -k "restricted or remaps_cls"`: 4 passed.
- `ruff format --check` and `ruff check` passed.
- Not tested on Windows or Linux.
```

The section headings follow PR #26935 and are a suggested structure, not mandatory Ultralytics fields.

上述章節沿用 PR #26935 的結構，是建議格式，不是 Ultralytics 必填欄位。
