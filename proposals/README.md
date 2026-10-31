# 貢獻提案 / Contribution proposals

本目錄的提案與 PR 草稿均提供繁體中文及英文版本，兩版的範圍、證據與驗證狀態須一致。中文供閱讀與討論；正式提交上游只使用英文。依 ISO 24495-1 的淺白寫作原則編修，先說目的，再交代證據與下一步。

Each proposal and PR draft includes Traditional Chinese and English versions with matching scope, evidence, and validation status. Chinese is for local review and discussion; only English is used for upstream submissions. Follow ISO 24495-1 plain-language principles: state the purpose first, then provide evidence and next steps.

## 可行方向 / Feasible directions

依建議處理順序排列（2026-10-29）。/ In recommended order (2026-10-29).

| 提案 / Proposal | 類型 / Type | 狀態 / Status | 下一步 / Next step |
| --- | --- | --- | --- |
| [T01／T05：weights_dir 文件澄清 / Clarify weights_dir documentation](weights-dir-docs/README.md) | 文件 / Docs | PR #26935 已於 2026-10-30 合併；維護者把 10 行說明改寫為表格列加一句註記，最終 +3/−1 / PR #26935 merged 2026-10-30; maintainer folded the 10-line note into the table row plus one sentence (+3/−1) | 完成 / Done |
| [T07：說明 maps 對未評估類別的填值 / Explain maps filler for unevaluated classes](maps-docs/README.md) | 文件 / Docs | 已開 PR #26955，已核可（2026-10-30）/ PR #26955 open, approved (2026-10-30) | 維護者要求後，`d2fd73703` 已改完其餘 7 處並回覆；等審查 / Remaining 7 places done in `d2fd73703` at maintainer request; await review |
| [#26707 延伸：安全載入無法載入自訂分類轉換 / Restricted loading rejects custom classify transforms](safe-load-custom-transforms/README.md) | 錯誤回報 / Bug report | PR #26949 已於 2026-10-30 合併，issue #26943 關閉 / PR #26949 merged 2026-10-30; issue #26943 closed | 完成 / Done |
| [T13：更新 COCO JSON 指南的快取說明 / Update the COCO JSON guide's cache note](coco-json-cache-docs/README.md) | 文件 / Docs | 已開 PR #26960（2026-10-30）/ PR #26960 open (2026-10-30) | 等審查 / Await review |
| [T14：修正 mask 轉換工具的輸入格式說明 / Correct the mask converter's input format](mask-converter-docs/README.md) | 文件 / Docs | 已開 PR #26971（2026-10-31）/ PR #26971 open (2026-10-31) | 等審查 / Await review |

## 已評估、不建議投入 / Evaluated and set aside

| 方向 / Direction | 理由 / Reason |
| --- | --- |
| [T14 候選 2：predict 來源表與 `batch` 說明 / predict source table and `batch` description](../research/tutorial-audit/records/T14.md) | 暫緩：沒有使用者回報，先看候選 1 的審查結果 / On hold: no user report; revisit after candidate 1's review |
| #26707 分類裁切的文件缺口 / docs gap for classify crop | 已驗證：文件範例在預設載入下完整 / Verified complete under default loading |
| T03-B `masks` 為 `None` / `masks` is `None` | 文件已標示 `Masks, optional` / Already documented as optional |
| T02-B 信心分數四捨五入 / Score rounding | 正常的顯示行為 / Normal display behavior |
| #26324 MPS 計時 / MPS timing | 需要 Apple 真機 / Needs Apple hardware |
| T10 ONNX 較慢 / ONNX slower | 需要控制變因的效能研究，成本高 / Needs controlled benchmarking |
| [內建 SHAP 解釋 / Built-in SHAP explanations](shap-explainability/README.md) | 已有 LayerCAM；功能 PR 須先取得 issue 同意，且新增依賴與 50 行門檻高 / LayerCAM exists; feature PR needs approved issue, high bar for new deps and 50+ lines |

依據見研究書[第四章研究卡](../research/contributing/docs/roadmap.md)與 [tutorial audit](../research/tutorial-audit/README.md)。/ Evidence: research book chapter 4 and the tutorial audit.

這些是研究草稿，不代表已實作、驗證或取得維護者同意。

These are research drafts, not evidence of completed implementation, validation, or maintainer approval.
