# mini-sprints — 設計說明

這份寫給人：說明這個 skill 的設計動機、想解決的問題、以及檔案結構背後的取捨。
給 Claude 的操作指令在 [SKILL.md](SKILL.md)，迭代史在 [CHANGELOG.md](CHANGELOG.md)。

## 要解決的問題

工作任務來自一個**工作單元**（work unit）——常見是 Jira ticket，但也可能是一份
plan/設計文件、或一段已討論過的需求。把 requirement → design → implementation
視為一個週期時，AI 常落入**瀑布式**流程：縝密討論需求 → 生成龐大實作計劃 → 一口氣
實作完。兩個痛點：

- **人的認知負擔。** AI 會一口氣展開大量決策細節，人沒辦法一次接收、判斷這麼多
  資訊；加上 AI 容易自行幻想補全許多規格，人往往難以從中看出重點在哪。
- **AI 回撤的代價高。** 一口氣生成完整規劃後，只要有些前提改變，要 AI 回頭反覆修改後
續衍伸文件的效果往往很差——不如「漸進式收斂」，在大架構確認的前提下，每次只往前推確定的
一小段。

## 用起來長什麼樣

一個工作單元跑到一半時，`mini-sprints/` 大致長這樣（以 Jira ticket AEG-155「串流遙測
API」為例，已切三刀、第三刀進行中）：

```
mini-sprints/                        # repo root，已 gitignore（本機工作區，不進版控）
├── CLAUDE.md                        # 「現在在 AEG-155 iteration 3；動 schema 前先讀 design.md」
└── AEG-155/
    ├── specs/
    │   ├── requirements.md          # 來源=Jira AEG-155；Core Spec 已定，Derived 還留兩處 (待釐清)
    │   └── design.md                # 串流架構、schema 版本策略——拆刀前就先定好的整體骨架
    ├── iteration_1/                 # 第一刀：API contract
    │   ├── scope.md
    │   └── plan.md
    ├── iteration_2/                 # 第二刀：schema + migration
    │   ├── scope.md
    │   └── plan.md
    ├── iteration_3/                 # 第三刀：中間實作（進行中）
    │   ├── scope.md
    │   └── plan.md
    └── retrospectives/
        ├── conversations.md         # 3 筆：2 轉折 1 阻礙，schema 命名反覆被標「復發」
        ├── iterations.md            # iteration 1–2 的 outcome 敘事
        └── reflections.md
```

讀法：`specs/` 是一路保持最新的活文件；每個 `iteration_N/` 是一刀的固定 scope；
`retrospectives/` 累積「哪裡卡過、學到什麼」，`CLAUDE.md` 把跨單元的狀態與原則濃縮給
下一個 session 的 AI。實際的欄位與模板定義見 [SKILL.md](SKILL.md)。

## 設計取捨

**核心是 sprint 的精神**：不要過早預測不確定性，聚焦於確定的範疇，靠大量迭代逐步
收斂後續設計。單一工作單元內無法真的跑 sprint，所以這個 skill 用一套檔案結構來
**模擬** sprint——每個 iteration 刻意只做一個有意義的邊界，讓使用者 review 時認知
負擔最小。

幾個關鍵決策：

- **spec 是活文件，不是一次定稿。** `requirements.md` 允許帶著「待釐清」的留白隨
  iteration 補完；只有每一刀的 `scope.md` 要求語意精準。整體需求可以模糊，每一刀
  的 scope 必須清晰——這是避免早期過度預測失準的關鍵。
- **iteration 邊界＝不變量。** 同一 scope 內反覆打磨仍是同一刀；回頭改已封板的階段
  就當新一刀。讓「還算同一 iteration 嗎」有明確判準，不靠感覺。
- **一刀一次交付。** 一個 iteration 整批盤點 → 一起做 → 一起 review → 一次交付，不
  邊做邊零碎 commit，否則會把一刀切碎、失去 iteration 邊界。
- **收尾整合 review。** 切小刀有結構盲點：每刀 review 都是局部的，沒有任何一步看
  「整合後的整體」。所以交付整個單元前補一次全局 review（完整性 vs plan、整合衛生
  vs base branch）。這一步是首跑實戰中補上的（見 CHANGELOG）。
- **conversations.md 的信心/復發階梯。** retrospective 要不要把某個教訓升格成原則，
  設計成**有資料可查**（同根因復發幾次、信心暫定還是確立），而不是靠臨場記憶判斷。
- **self-improve 的兩道閘。** skill 是團隊共享物，什麼教訓夠格回饋進 skill 本身，設
  了明確門檻（屬流程結構 + 是結構契約），避免它變成什麼都收的雜物櫃。

## 演進脈絡

這個 skill 初版把 Jira ticket 當前提。首次實跑的工作單元（flight-anchored-issues）
context 卻來自 plan 文件、根本沒有 ticket，於是「ticket」一般化為「工作單元」，Jira
降為三種 context 來源之一。收尾整合 review、一刀一次交付、self-improve 兩道閘也都是
那次 retrospective 蒸餾出來的。詳見 [CHANGELOG.md](CHANGELOG.md)。
