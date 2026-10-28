# 1. 貢獻規則與方法

## 先判斷貢獻種類

貢獻不只寫程式。把一個模糊回報縮成公開模型、公開輸入及確切環境的重現，能讓維護者作出判斷；指出文件範例與現行 API 不一致，也能形成小而完整的修正。官方同時接受 bug 回報、文件修改與 PR review。[貢獻入口](https://docs.ultralytics.com/help/contributing/)

| 類型     | 最少需要的證據                                   | 何時先停下來                                 |
| -------- | ------------------------------------------------ | -------------------------------------------- |
| Bug 修正 | 修改前能重現、修改後恢復契約，相關既有路徑仍正常 | 只有私人權重或缺少預期行為                   |
| 文件修正 | 文件原句、對應程式碼與可執行範例                 | 修改生成的 reference，卻沒改 docstring owner |
| 效能改善 | 同設備、同輸入、同精度與相同輸出品質的比較       | 只是單次計時，或改了全域設定但未驗回歸       |
| 功能提案 | 多使用者需求、既有介面不足及維護者同意           | 只滿足自己的 pipeline，且需新增參數／依賴    |
| 協助排查 | 環境資訊、最小輸入與可排除假設                   | 尚未確認就把使用問題定性為產品 bug           |

表中的門檻是本書的執行建議；規範基礎為 [CONTRIBUTING.md](https://github.com/ultralytics/ultralytics/blob/main/CONTRIBUTING.md) 與研究基準的 [AGENTS.md](https://github.com/Echoslayer/ultralytics/blob/bb3e1550dbb819bd9846d4c99f368aebe8792a0e/AGENTS.md)。

## 兩份規範要一起讀

`CONTRIBUTING.md` 對首次貢獻約超過 50 行的實質修改持保留態度，文件／docstring／格式為例外；`AGENTS.md` 的 review gate 則將超過 50 行「淨新增非文件程式碼」以及新參數、新依賴列為高門檻。兩者的計數方式不同，不能把淨新增 49 行當作保證通過。最可靠的做法是單一目的、最小完整 diff，並說明為何不能再縮。[範圍規範](https://github.com/ultralytics/ultralytics/blob/main/CONTRIBUTING.md)；[研究基準規則](https://github.com/Echoslayer/ultralytics/blob/bb3e1550dbb819bd9846d4c99f368aebe8792a0e/AGENTS.md)

測試也有相似差異：一般貢獻指南要求適當驗證，這份 checkout 的代理規範預設不新增測試，只有未覆蓋且高風險的路徑才補最少 coverage。因此先找既有測試並執行真實路徑，不要為了讓 diff 看起來完整而新增大量 mock。

## 從線索到修正的七步

1. 搜尋同樣症狀、相關關閉 issue 和正在進行的 PR。閱讀結案理由，避免重做已解決的問題。
2. 記錄版本與基準 SHA；確認 fork 與 upstream 是否同步。
3. 把輸入縮成可公開分享的最小案例，留下 expected／actual 與完整錯誤。
4. 搜尋呼叫者，找到真正觀察或擁有行為的模組。在 owner 修正，而不是在下游補例外或初始化旗標。
5. 列出會受影響的 task、模式、平台、輸出格式與文件，再實作最小修正。
6. 跑相關既有檢查，保留修改前後的結果。效能題同時驗輸出品質。
7. 以小型 PR 說明問題、行為變化與驗證結果，跟進 bot 與人工 review。

第 1–3 步呼應 [官方 MRE 方法](https://docs.ultralytics.com/help/minimum-reproducible-example/)；owner 與最小 diff 原則來自 [AGENTS.md](https://github.com/Echoslayer/ultralytics/blob/bb3e1550dbb819bd9846d4c99f368aebe8792a0e/AGENTS.md)。

## 分支與 PR 的實際安排

目前 `origin` 是 `https://github.com/Echoslayer/ultralytics.git`，不是官方 repo。這次研究分支從 `origin/main` 建立，保留原始 checkout。日後正式貢獻時先查 `git remote -v`，若沒有官方 remote，再新增 `upstream` 並 fetch；新工作樹應以當時官方 main 為基準。本書沒有自動修改 remote，也沒有推送。

研究筆記留在研究分支；每一個正式修正獨立開 branch。不要把整本書或出版依賴帶入上游修正 PR。推送前先拉取遠端更新並 rebase；上游 bot 可能推送格式或標頭 commit，不要覆寫他人的修改。[工作樹與審查規則](https://github.com/Echoslayer/ultralytics/blob/bb3e1550dbb819bd9846d4c99f368aebe8792a0e/AGENTS.md)

## 審查時真正要交代的內容

一份有效 PR 描述可以很短：「在什麼輸入與環境下，原本哪個行為錯了；現在如何修正；跑了什麼驗證；哪些平台未覆蓋」。將問題連回 issue，避免只有「improve robustness」之類無法驗收的描述。所有自動建議都應閱讀，採用或說明不適用的原因；CI 綠燈不是完整 review 的替代品。[自動審查說明](https://github.com/ultralytics/ultralytics/blob/main/CONTRIBUTING.md)

CLA 是合併前流程，請本人閱讀文件並依 bot 指示處理。本輪只有研究，沒有代簽。社群溝通遵守 [Code of Conduct](https://docs.ultralytics.com/help/code-of-conduct/)；不要把未重現的推測寫成已確認根因。
