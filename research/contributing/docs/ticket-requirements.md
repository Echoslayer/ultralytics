# 6. 外部貢獻要先開 Jira 嗎？

**目前查到的公開規範，沒有要求外部貢獻者先開 Jira 或 Linear。** 你主要使用 GitHub 議題（issue）與合併請求（PR）。新功能有明確的事前討論要求；小型錯誤或文件修正，則未查到一律先開單的規定。

查核日期：**2026-10-28**。本章回答公開開源貢獻流程，不推斷公司的私人工作系統。

## 依修改種類決定要不要先開議題

| 你要做什麼？   | 公開規範要求                                                                     | 建議的第一步                                             |
| -------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------- |
| 新增功能       | 專案 `CONTRIBUTING.md` 要求先有 GitHub 功能提案，充分討論並取得維護者明確同意    | 搜尋既有提案；若沒有，再說明用途、受益對象與最小範圍     |
| 修復可重現錯誤 | 官方要求回報附最小範例、環境與預期／實際結果；未寫成所有修正 PR 都必須先另開議題 | 已有議題就補重現證據並在 PR 連回；根因或預期不明時先討論 |
| 小型文件更正   | 查到的流程允許準備修改、驗證後提出 PR，未另列 Jira 或事前議題門檻                | 找到文件來源，附原句、正確行為與驗證方式                 |
| 已有同題議題   | 模板要求先搜尋，避免重複回報                                                     | 在既有討論延續，不為自己另開同題單                       |

新功能的要求以[專案貢獻規範](https://github.com/ultralytics/ultralytics/blob/main/CONTRIBUTING.md)為依據。錯誤與文件流程見[官方貢獻指南](https://docs.ultralytics.com/help/contributing/)。查重要求見[功能提案模板](https://github.com/ultralytics/ultralytics/blob/main/.github/ISSUE_TEMPLATE/feature-request.yml)與[錯誤回報模板](https://github.com/ultralytics/ultralytics/blob/main/.github/ISSUE_TEMPLATE/bug-report.yml)。表中的「建議」是本書的操作判斷。

「沒有一律先開單的規定」不等於任何修改都能直接送。若修正會改變既有行為、增加參數或擴大架構，先確認維護者是否認同方向，能避免投入後才發現範圍不合適。

功能 PR 的實際評估案例見 SHAP 評估（`proposals/shap-explainability/README.md`）（2026-10-30）：上游已有 LayerCAM，維護者兩次建議在外部包裝，因此結論是先開功能 issue，不直接送 PR。

## 已關閉的 issue，仍可能支持文件改善

關閉狀態只告訴你討論已結束，不能單靠它判斷是否還有文件缺口。先讀解答、關閉原因與相關 PR，再決定是否貢獻。

2026-10-29 核讀的 [#18435](https://github.com/ultralytics/ultralytics/issues/18435) 是下載路徑提問，被標為 #17513 的重複議題。維護者解釋 `weights_dir` 的查找用途並提供明確路徑範例，提問者於 2024-12-31 自行關閉。這不是合併修正後關閉的 bug，因此文件 PR 應引用 `Related to #18435 and #17513`，不要宣稱修復尚未解決的程式錯誤。

[PR #24150](https://github.com/ultralytics/ultralytics/pull/24150) 曾嘗試改變下載目的地，但未合併；討論涉及 CI 與校正資料路徑。後續 [#26935](https://github.com/ultralytics/ultralytics/pull/26935) 選擇解釋既有行為，是不同的修改範圍。舊 PR 未合併不能直接推論文件澄清也被拒絕。

新功能仍須先開功能 issue、充分討論並獲維護者明確同意；小型文件修正沒有一律先開 issue 的要求。已有相同問題時，可直接在文件 PR 附舊議題作背景，避免再開重複單。這是依[官方規範](https://github.com/ultralytics/ultralytics/blob/main/CONTRIBUTING.md#feature-prs)與上述案例整理的建議，不是先開單比例的統計。

## 公司內部管理要求，不等於外部貢獻要申請帳號

官方開發手冊同時涵蓋員工與貢獻者，要求工作有明確負責人，並評估影響、優先順序與風險。它要求在議題、PR、文件或操作手冊保留決策，也區分外部貢獻者建立個人副本、員工同步有寫入權限的專案。[開發工作流程](https://handbook.ultralytics.com/workflows/development)

這些是責任與紀錄要求，不能推導成「外部貢獻者必須開公司 Jira」。本輪查到的公開開發流程沒有指定 Jira 或 Linear，也沒有提供外部貢獻者必備的帳號申請步驟。這只能支持**未查到公開要求**，不能證明公司內部從未使用這些工具。

官方議題入口連到文件、論壇、Discord 與 Reddit，沒有把 Jira 列為外部入口。[議題入口設定](https://github.com/ultralytics/ultralytics/blob/main/.github/ISSUE_TEMPLATE/config.yml)

## 身分確實影響官方寫明的審查優先順序

專案貢獻規範明確表示，已有可靠貢獻紀錄的人，通常獲得較高審查優先順序。它沒有設定固定次數門檻；在其他知名開源專案的良好紀錄，也可能被考慮。這是審查優先順序，不是保證合併。[既有貢獻者規範](https://github.com/ultralytics/ultralytics/blob/main/CONTRIBUTING.md#established-contributors)

同一份規範要求首次貢獻範圍小。約超過 50 行的實質修改通常不受鼓勵，但文件、程式內說明與格式修改可例外；首次貢獻也不鼓勵直接做新功能。[首次貢獻者規範](https://github.com/ultralytics/ultralytics/blob/main/CONTRIBUTING.md#first-time-contributors)

開發手冊要求審查者在一至兩個工作天內審查或轉交。這是工作目標，不能當成每一筆外部 PR 的回覆保證，更不是合併期限。[審查者指引](https://handbook.ultralytics.com/workflows/development#for-reviewers)

## 統計身分時，不要把 GitHub 標籤當成僱用關係

GitHub 的 `author_association` 表示帳號與專案的關係，不直接表示職稱或僱用狀態：

| 公開值                   | GitHub 的意思              | 不宜直接推論                     |
| ------------------------ | -------------------------- | -------------------------------- |
| `MEMBER`                 | 所屬組織的成員             | 一定是公司員工                   |
| `COLLABORATOR`           | 受邀協作這個專案           | 一定是內部團隊                   |
| `CONTRIBUTOR`            | 曾向專案提交程式碼         | 已達官方所稱的可靠貢獻者程度     |
| `FIRST_TIME_CONTRIBUTOR` | 此前未向此專案提交程式碼   | 沒有其他開源經驗                 |
| `FIRST_TIMER`            | 此前未向 GitHub 提交程式碼 | 可與所有新帳號或 `NONE` 混為一組 |
| `NONE`                   | 沒有上述專案關聯           | 一定是第一次提出 PR              |
| `OWNER`                  | 專案擁有者                 | 能單獨推定其公司職務             |

來源：[GitHub 的關聯欄位定義](https://docs.github.com/en/graphql/reference/issues#commentauthorassociation)。因此，合併率研究應用「GitHub 組織成員／協作者」等可觀察名稱；若要研究員工與外部人士，還需要獨立且可靠的身分證據。

## 查核範圍與下一步

本輪查閱公開貢獻指南、專案 `CONTRIBUTING.md`、開發手冊與議題模板，並搜尋官方網域中的 Jira／Linear 要求。網頁可能有快取；文件網站與專案檔案的內容也不完全相同，專案特有的首次貢獻與新功能規則以 `CONTRIBUTING.md` 為本章依據。

本地研究版本沒有專案內的 PR 模板。另已透過 GitHub API 讀取[組織共用 PR 模板](https://github.com/ultralytics/.github/blob/main/PULL_REQUEST_TEMPLATE.md)：它要求查重、說明修改、處理 CLA；如果 PR 對應現有議題，應附議題連結。模板沒有要求先開 Jira。未查閱私人內部系統、未向維護者詢問，也未開任何追蹤單。

對你而言，下一步是選一個小型可重現問題，搜尋既有 GitHub 議題與 PR。只有新功能或範圍尚未確認的變更，才先把討論收斂到維護者同意的方向；目前不需要為此另申請 Jira。
