# 4. 選題與行動路線

## 先選可驗證的題目

本輪最值得先調查的是 **#26707 的分類前處理文件／範例缺口**。理由不是它已被確認為 bug，而是能使用人工產生的公開影像檢查既有擴充點，較容易得到可審查的證據。若既有文件已充分說明且範例可跑，就結束此題，不為了提交 PR 而製造新設定。[案例與維護者回覆](https://github.com/ultralytics/ultralytics/issues/26707)

第二條是 **#26324 的計時與 backend 效能研究**，但 MPS 部分需要 Apple 真機，目前不能因為工作目錄在 Windows 就假定有設備。OpenVINO CPU 預取已合併，不重做；先驗證剩餘路徑、查重 PR，再投入。[討論](https://github.com/ultralytics/ultralytics/issues/26324)；[已合併 PR](https://github.com/ultralytics/ultralytics/pull/26897)

這個排序是本書推論。完整來源及排除理由見 [案例章](issues-and-community.md)。

## 四個階段，不用承諾固定週數

| 階段                   | 具體工作                                         | 完成證據                           | 停止／換題條件                        |
| ---------------------- | ------------------------------------------------ | ---------------------------------- | ------------------------------------- |
| A：看懂規範與版本      | 讀規範、確認 upstream SHA、挑一題查最新討論與 PR | 一張來源完整的研究卡               | 已修好、已有同範圍 PR、維護者不支持   |
| B：得到可重現證據      | 固定輸入與環境，記錄 expected／actual            | 可獨立執行的命令、輸入與結果       | 缺設備、私人資料無法替換、無法重現    |
| C：找到最小 owner 修正 | 搜尋所有 caller、列影響範圍、比較修改前後        | 小 diff 與相關既有驗證             | 需要新 API 或架構變更，先回到提案討論 |
| D：正式貢獻            | 新建乾淨分支、撰寫英文 PR、跟進 review           | 遠端精確 head 的驗證與 review 紀錄 | 新結果推翻根因時，回到 B              |

本輪完成研究書，尚未執行 B、C、D。上表是下一輪操作路線，不是已完成紀錄。

## 第一個 probe：分類前處理

目標是確認長寬比極端圖片的邊緣內容，在 train、val、predict 各路徑是否符合選定 transform 的契約。準備寬圖、長圖與正方形圖，在四角放明顯標記；保存「真正輸入模型前」的張量或可視化。比對現行預設與官方建議的 custom transforms，避免只展示 letterbox 輸出卻漏掉後續 crop。

若三條路徑都可透過現有 hook 正常達成，接著搜尋文件是否已存在同樣例子；只有確有缺口時才提最短範例。若有一條路徑不能保持同樣設定，先縮成該路徑的 MRE，不能直接跳到新增全域參數。這套 probe 是本書建議，尚未執行。[#26707](https://github.com/ultralytics/ultralytics/issues/26707)

## 研究卡範本

每次選題可在本章末尾新增一節，先不建立新的自動化 tracker。以下欄位足夠判斷是否值得進入修復：

```text
題目與來源 URL：
讀到的最後留言日期／查核時間：
issue 狀態、相關 PR 與是否已有參與者：
基準 SHA、套件版本、工作樹是否乾淨：
OS、Python、torch、backend、硬體：
預期行為及其規範來源：
最小公開輸入與執行命令：
實際輸出／錯誤／量測紀錄：
已排除的假設：
owner、caller 與受影響 task／模式：
最小修正方向：
驗證與停止條件：
決定：繼續／等待／排除，以及理由
```

## 如何搜尋，而不被標籤帶著走

在官方 repo 搜尋下列查詢，再用元件、症狀與錯誤字串細化。這些是查詢配方，不是本輪已完整遍歷的結果集。

```text
repo:ultralytics/ultralytics is:issue is:open label:bug
repo:ultralytics/ultralytics is:issue "ClassifyLetterBox"
repo:ultralytics/ultralytics is:pr "MPS" "Profile"
repo:ultralytics/ultralytics is:pr is:merged "prefetch"
repo:ultralytics/ultralytics is:issue is:closed "你的錯誤字串"
```

每輪讀一筆 open issue、一筆同領域 merged PR，再看是否有 closed／rejected 方案。這樣能同時理解使用者需求和維護者接受邊界。不要只以 `good first issue`、留言數或行數決定投入。

## 未來留言或 PR 的內容草稿

完成重現後，可用以下英文結構整理證據；它是草稿範本，本輪沒有發送：

```text
I reproduced <specific behavior> on <commit and environment> using <public input>.
Expected: <documented contract>.
Observed: <actual output>.
Minimal reproduction: <command or short snippet>.
The behavior appears to originate in <owner>, because <evidence>.
Validation: <before/after result and related paths checked>.
Not yet checked: <specific platform or integration>.
```

能填完這些欄位，通常比先寫大量程式更接近一筆可審查的貢獻。是否採納仍由維護者依實際 diff、需求與維護成本判斷。
