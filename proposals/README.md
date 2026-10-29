# 貢獻提案 / Contribution proposals

本目錄的提案與 PR 草稿均提供繁體中文及英文版本，兩版的範圍、證據與驗證狀態須一致。中文供閱讀與討論；正式提交上游只使用英文。依 ISO 24495-1 的淺白寫作原則編修，先說目的，再交代證據與下一步。

Each proposal and PR draft includes Traditional Chinese and English versions with matching scope, evidence, and validation status. Chinese is for local review and discussion; only English is used for upstream submissions. Follow ISO 24495-1 plain-language principles: state the purpose first, then provide evidence and next steps.

## 可行方向 / Feasible directions

依建議處理順序排列（2026-10-29）。/ In recommended order (2026-10-29).

| 提案 / Proposal | 類型 / Type | 狀態 / Status | 下一步 / Next step |
| --- | --- | --- | --- |
| [T01／T05：weights_dir 文件澄清 / Clarify weights_dir documentation](weights-dir-docs/README.md) | 文件 / Docs | 已開 PR #26935，已核可，待合併 / PR #26935 open, approved | 等合併；之後對照第九章的回應時間 / Await merge |
| [T07：說明 maps 對未評估類別的填值 / Explain maps filler for unevaluated classes](maps-docs/README.md) | 文件 / Docs | 已查證上游與既有議題 / Upstream and issues checked | 在最新 main 重跑 COCO8，再開 PR / Rerun on latest main, then PR |
| [#26707 延伸：安全載入無法載入自訂分類轉換 / Restricted loading rejects custom classify transforms](safe-load-custom-transforms/README.md) | 錯誤回報 / Bug report | 已開 issue #26943 / Issue #26943 filed | 等維護者回覆 / Await maintainer reply |

## 已評估、不建議投入 / Evaluated and set aside

| 方向 / Direction | 理由 / Reason |
| --- | --- |
| #26707 分類裁切的文件缺口 / docs gap for classify crop | 已驗證：文件範例在預設載入下完整 / Verified complete under default loading |
| T03-B `masks` 為 `None` / `masks` is `None` | 文件已標示 `Masks, optional` / Already documented as optional |
| T02-B 信心分數四捨五入 / Score rounding | 正常的顯示行為 / Normal display behavior |
| #26324 MPS 計時 / MPS timing | 需要 Apple 真機 / Needs Apple hardware |
| T10 ONNX 較慢 / ONNX slower | 需要控制變因的效能研究，成本高 / Needs controlled benchmarking |

依據見研究書[第四章研究卡](../research/contributing/docs/roadmap.md)與 [tutorial audit](../research/tutorial-audit/README.md)。/ Evidence: research book chapter 4 and the tutorial audit.

這些是研究草稿，不代表已實作、驗證或取得維護者同意。

These are research drafts, not evidence of completed implementation, validation, or maintainer approval.
