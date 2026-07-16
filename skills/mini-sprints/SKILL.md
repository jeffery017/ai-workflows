---
name: mini-sprints
description: >
  迭代式開發工作流，把單一工作單元（work unit；可能是 Jira ticket、plan/設計文件、
  或一段已討論的需求）的 requirement → design → implementation 拆成「刻意限縮範圍」
  的小迭代（mini-sprint），避免一口氣產出龐大實作計劃與難以 review 的巨量 code。
  用於：使用者執行 `/mini-sprints`（或帶 plan / status / retro 參數）、說「我們來規劃
  這個 ticket / 這份 plan」「把這次討論整理成需求」「規劃下一個 iteration」「開一個
  新的 mini-sprint」「更新 retrospective」「現在做到哪了」。在以單一工作單元為範圍、
  需要 spec-first 並逐步收斂設計的開發任務中主動使用。
---

# mini-sprints — 單一工作單元內的迭代式開發工作流

## 為什麼存在

工作任務來自一個**工作單元**——常見是 Jira ticket，但也可能是一份 plan/設計文件、或
一段已討論過的需求。把 requirement → design → implementation 視為一個週期時，
常見的 AI 工作流是**瀑布式**的：縝密討論需求 → 生成龐大實作計劃 → 一口氣實作完。
問題在於：

- 龐大的 implementation plan 讓人難以消化、巨量實作細節難以 review。
- 需求必然有疏漏、設計必然有瑕疵 —— 很多問題要到實作階段才浮現。設計、規格、
  架構在實作中變更，**實屬正常**。

解法是 **sprint 的精神**：不要過早預測不確定性，聚焦於確定的範疇，靠大量迭代逐步
收斂後續設計。單一工作單元內無法真的跑 sprint，所以這個 skill 用一套檔案結構來
**模擬** sprint：每個 iteration 刻意只做一個有意義的邊界，讓使用者 review 時認知
負擔最小。

**核心心法**：你不是在「規劃完整方案然後執行」，而是在「選一個小切片、做、收集
回饋、再規劃下一刀」。抗拒一次做完的衝動。

## 檔案結構

```
mini-sprints/                          ← repo root，已 gitignore
├── CLAUDE.md                          ← 跨工作單元的 AI briefing：現在在哪個單元 + 蒸餾原則
└── AEG-155/                           ← 工作單元代號：Jira key（AEG-155）或描述性 slug（flight-anchored-issues）
    ├── specs/
    │   ├── requirements.md            ← 最新、最完整的需求定義（漸進補完）
    │   ├── design.md                  ← 架構與設計決策（任務需要才建）
    │   └── <其他 helper 文件>         ← 視任務性質自由增加
    ├── iteration_1/
    │   ├── scope.md                   ← 這個 iteration 的範圍 + 與上次的需求變更
    │   ├── plan.md                    ← scope / todo / definition-of-finished
    │   └── <其他 helper 文件>
    ├── iteration_2/
    │   └── ...
    └── retrospectives/
        ├── conversations.md           ← 表格：導致重工/轉折或卡關的事件與根因
        ├── iterations.md              ← 每個 iteration 的敘事摘要（段落感）
        └── reflections.md             ← 跨 iteration 的觀察與原則
```

**spec 是活文件**：`specs/` 裡的文件在迭代過程中**必須永遠保持最新**。需求變更時，
先更新 `requirements.md`（與 `design.md`），再規劃 iteration —— 不要讓 spec 落後於
實作。使用者可在 `specs/` 自由新增其他文件，同樣需保持最新。

## 啟動：每次執行 `/mini-sprints` 都先做

1. 確認 `mini-sprints/` 在 repo root 存在，不存在就建立。
2. 確認 `.gitignore` 含 `mini-sprints/`，沒有就加上（這是本機工作區，不進版控）。
3. 決定**工作單元代號**（即下方 `<UNIT>` 佔位符／目錄名）：branch 名含 Jira key 就
   用它（`AEG-155-streaming-...` → `AEG-155`）；否則用描述性 slug（從 branch 名或任務
   內容取，如 `flight-anchored-issues`）。拿不準就問使用者。context 來源不限 Jira——也
   可能是 plan/設計文件或本次討論。
4. 讀 `mini-sprints/CLAUDE.md`（跨工作單元 briefing，存在的話）了解全域狀態與已蒸餾
   的原則。
5. 若 `mini-sprints/<UNIT>/` 已存在 → 這是**接續既有工作單元**：讀取該單元的
   `specs/requirements.md`、`retrospectives/iterations.md`、以及編號最大的
   `iteration_N/scope.md`，給一段狀態摘要：「你現在在 <UNIT> 的 iteration N，
   上次做到 X，待 review / 待實作的是 Y」。然後依使用者帶的參數或意圖進入對應階段。
6. 若不存在 → 這是**新工作單元**，進入 Phase 1。

## 模式（slash command 參數）

- 無參數：啟動流程。新工作單元 → Phase 1；既有工作單元 → 給狀態摘要後待命。
- `plan`：進入 Phase 2，提案並規劃下一個 iteration 的 scope。
- `status`：只讀。給當前 iteration 狀態 —— 已完成、待 review、待實作的項目。
- `retro`：進入 Phase 4，更新 retrospective 文件並蒸餾原則到 `CLAUDE.md`。

## 階段交界紀律（貫穿全程）

每個階段收尾時（define requirements 完、scoped implementation 完），**不要逕自往下
一階段衝**。先停下來，把這階段的產出攤給使用者，明確問「這樣對嗎？有沒有要調整
的？」確認他滿意，再前進。階段交界是收斂的關卡，不是過場。

這條紀律的精神跟整個 skill 一致：每一刀做完就收斂、確認，再開下一刀。

---

## Phase 1 — Requirements（新工作單元）

前提：使用者通常**已在當前 session 完整討論過這個任務**，執行 `/mini-sprints` 時
context 已足夠。你的工作是**整理**，不是從零訪談。

**漸進式定義需求 —— 這是核心精神。** 不要求一次把所有需求定義到 100% 清楚：那不
切實際，而且早期過度預測的需求到後期容易失準（這正是 mini-sprint 要避免的瀑布式
陷阱）。`requirements.md` 是**活文件**，允許 Core / Derived Spec 一開始就帶著
「尚未釐清」的留白，隨 iteration 推進逐步補完。真正需要**語意精準、覆蓋完整**的，
是每個 iteration 的 `scope.md` —— 因為那是即將動手的確定範疇。換句話說：整體需求
可以模糊，但每一刀的 scope 必須清晰。

1. 確認 context 來源並指向它（不複製內容進來）：**Jira ticket** → 用 jira skill /
   Atlassian MCP 抓，**不需要**把 description / AC / labels 逐字複製進 `requirements.md`，
   `## 來源` 段只留 key + title + 連結，細節靠 jira skill 隨時取用；**plan/設計文件** →
   `## 來源` 段留檔案路徑，讓讀者直接去讀；**純討論** → 註明「本次討論」。原則一致：
   讓使用者與後續 session 的 agent 從來源與這份文件的脈絡讀起，`requirements.md` 不當副本。
2. 把當前 session 的討論整理成 `specs/requirements.md`（模板見下），允許留白。
3. **`## Context` 必須白話、精簡**：用一般人能懂的話講清楚這個任務要解決什麼問題，
   不要堆術語、不要長篇。其餘段落可以技術性。
4. **不要輕易往下一階段（實作）衝。** 整理需求時，若發現某處定義模糊、但又屬於
   即將動手的範疇，**主動向使用者詢問規格定義**，把它釐清到夠精準。但仍 follow
   漸進式原則：**只對「即將進入 scope 的部分」追求高精度**，遠期、不確定的需求允許
   留白，別為了「問清楚」而把整張 spec 逼到 100%（那又落回瀑布陷阱）。判準是
   「這個釐清是不是下一刀需要的」。
5. 寫完後，**不要**自動進入 iteration 規劃。把整理好的 requirements 攤給使用者
   檢視，依「階段交界紀律」詢問有無問題，再提示：
   「確認後跟我說『規劃第一個 iteration』。」

### specs/requirements.md 模板

```markdown
# Requirements: <UNIT>

## 來源
<!-- 工作單元的 context 從哪來：Jira key / plan 文件路徑 /「本次討論」。只留指標，不逐字複製。 -->
<Jira key 或 plan 文件路徑 或「本次討論」> — <title 或一句話>  ·  <連結，若有>

## Context
<!-- 白話、精簡。這個任務要解決什麼問題，為什麼重要。 -->

## Core Spec
<!-- 必須做到的核心需求與關鍵行為。允許留白：尚未釐清處標 (待釐清)。 -->

## Derived Spec
<!-- 從 core spec 推導出的隱含需求、約束、邊界條件。同樣允許漸進補完。 -->

## Out of Scope
<!-- 明確排除，保持範圍乾淨 -->
```

---

## Phase 2 — Iteration Planning（`plan` 或使用者說「規劃 iteration」）

目標：選一個**刻意限縮**的切片，使產出的 code 落在一個有意義的邊界上，讓使用者
review 時聚焦、認知負擔低 —— 而不是一口氣塞進各種面向的實作。

### iteration 邊界的判準（參考性概念）

一個 iteration 必須有**固定而明確的 scope**，一旦定下就不該任意變動。據此判斷
「還算同一個 iteration」還是「該開新的」：

- **同一 scope 內反覆迭代 → 仍是同一個 iteration。** 實作過程中針對既定 scope 來回
  打磨、修正、調整，scope 沒變，就不另開 —— 這是正常的收斂，不是新一刀。
- **回頭改已通過的階段 → 視為新的 iteration。** 若已從 stage 1 進到 stage 2，之後
  因某個原因回頭修改 stage 1 的內容，這個「回修」就**直接當成新的 iteration**。因為
  它改的是先前已收斂、已 review 過的邊界，需要重新框 scope、重新交界。

精神：scope 是一個 iteration 的不變量。動到「已封板的範疇」就是跨進新一刀，而非在
舊一刀裡繼續。

1. **提案 scope，由使用者決定。** 不要自己拍板。根據 requirements 與已完成的部分，
   提出「這個 iteration 建議做 X」。建議的預設切法（任務適用時）：
   **API contract → schema → 中間實作**。但這只是建議，每個工作單元性質不同，
   最終由使用者選。
2. scope 敲定後，寫 `iteration_N/scope.md` 與 `iteration_N/plan.md`（模板見下）。
3. 若這次 iteration 涉及需求變更或釐清，**先更新 `specs/requirements.md`**
   （與 `design.md`，若有），再在 `scope.md` 的「需求變更」段落記下變更。
4. `N` = 既有最大 iteration 編號 + 1；第一個是 `iteration_1`。


### iteration_N/scope.md 模板

```markdown
# Iteration N Scope

## 本次涵蓋
<!-- 完整需求中，這個 iteration 處理的子集 -->

## 與上次 iteration 的需求變更
<!-- 需求更新、釐清、轉向；無則寫「無」 -->

## Definition of Finished
<!-- 這個 iteration 完成的具體判準 -->

## 明確延後
<!-- 不在本次、之後才做的項目 -->
```

### iteration_N/plan.md 模板

```markdown
# Iteration N Plan

## Scope 摘要
<!-- 一段話 -->

## Todo
- [ ] ...

## Definition of Finished
<!-- 從 scope.md 複述，實作時快速對照 -->

## Notes
<!-- 本次特有的架構決策、取捨、地雷 -->
```

---

## Phase 3 — Implementation

依 `iteration_N/plan.md` 實作。

### 1. 一個 iteration 是一次完整交付（收集完整、整批一起做，不要急著改 / 零碎交付）

實作完、使用者開始 review 時，面對 review 意見，**不要在第一時間直接動手修改**。
先確保使用者對當前版本的**所有意見都收集完備**，再一起規劃下一個 iteration —— 下一刀
可能包含「之前延後的需求」與「針對這版的修訂」。

理由：逐條即時修改會讓你和使用者陷入「東想一個改一個、西想一個改一個」的碎片化
節奏，失去 iteration 之間的段落敘事。先收斂意見，再規劃，才能保持每一刀的完整性。

**這條不只適用於「消化使用者回饋」，也適用於「自己的修正批次」。** 一個 iteration
（含收尾修正批）要先**整體盤點 scope → 一起實作 → 一起 review → 一次交付**，不要邊做
邊零碎交付（例如改完一段就立刻 commit），那會把一刀切碎、失去 iteration 邊界。交付 /
commit 的顆粒度細節依專案慣例，但「**一刀一次交付**」是通則。

當使用者對這個 iteration 的產出滿意（意見收斂、無待改），依「階段交界紀律」確認後，
再進 Phase 4 / 規劃下一刀。

**例外**：實驗性的小調整（尤其 UI），scope 沒變，不用另開 iteration，直接試。

### 2. 感知到轉折或阻礙時，主動提議記錄

你無法背景監控對話。但當你**意識到**以下情況，要在回覆中主動說「這個值得記進
conversations.md」並依該表欄位寫入一筆：

**方向轉折類**（導致重工）：
- 需求定義不清，導致已實作的東西要重寫。
- 架構決策在實作中途被推翻。
- 發現 spec 矛盾或遺漏，要回頭改 `requirements.md`。
- 使用者明確說「這個方向不對，換個做法」。
- **使用者要求重構 AI 產出的 code**（rename、refactor、搬結構）—— 代表初版的命名/
   結構不如預期，是品質訊號，要記（根因多半是 `品質不如預期` 或 `需求定義不清`）。
- **AI 自檢抓到**自己偏離（來源欄填 `AI 自檢`）—— 自己發現的也要記，不只記人抓到的。

**進度阻礙類**（沒重工，但卡住、效率低落）：
- 使用者在某個技術決策上**卡很久**、反覆來回難以收斂。根因可能是使用者對該技術
  掌握度不足、或 **AI 提供的資訊不精準/過時** 害對話空轉 —— 後者尤其要誠實記下，
  那是 AI 該改進的訊號。
- 設計/需求評估階段**耗時明顯偏長**：記下卡在哪、為什麼，作為日後量化「評估與定義
  需求的效率」的依據。

阻礙類記錄的價值不在「誰錯了」，而在累積後能看出**反覆卡關的模式**（某類技術老是卡、
某種需求老是難定義），進而改善流程或補強知識。

寫入時填好 `說明 / 根因 / 責任`；`信心` 預設 `暫定`，但**先掃既有列**：若同根因
之前出現過，這筆標 `復發`、並把信心拉到 `確立`（這正是 Phase 4 升格的依據）。

**不要記**順暢的良性對話：一兩個來回就收斂的追問、探討、一般 Q&A。這些是健康的，
記了只會稀釋訊號。判準是「**是否導致重工、或明顯拖慢進度**」，不是「有沒有討論」——
健康的探討很快收斂、不算阻礙；只有當討論**卡住、空轉、反覆**才升級成一筆紀錄。

### 3. 測量阻礙的代價

每記一筆阻礙類紀錄，順手量出那段卡關的代價：**對話來回次數 / 花費時間 / token
消耗**，填進卡點格。認出阻礙與測量是同一個動作的兩面，由你主導完成，無須使用者
開口（使用者也可主動說「**測量這段對話**」觸發，流程相同）。

記錄時機是浮動的：可能在卡關**還卡著時**就先記（已明顯空轉），也可能在**解決後**
或 Phase 4 回顧時才補。測量要配合這個時機，分兩種情形：

- **卡關尚未結束就記** → 量 起點→現在 的**開放區間**（省略 `--to-time`），先填一個
  初步數字；等卡關真正收斂時，回頭補上終點、更新該筆。
- **解決後才記** → 整段已閉合、起訖都在 context 裡，一次量完。

做法：

1. **定起訖。** 回看 context，判斷議題語意上從哪則訊息浮現（起）、到哪則收斂（訖，
   未結束就用當下），各取其**確切 timestamp**。
2. **跑腳本**（時間錨點模式較穩；純本機、幾乎不耗 token）：
   ```
   python3 .claude/skills/mini-sprints/scripts/span_tokens.py \
     --from-time <起點 timestamp> [--to-time <終點 timestamp>]
   ```
3. **回填並交代區間。** 把「N 來回 / M 分鐘 / ~K 新增 token」寫進卡點格，回覆裡
   附一句所取區間（「這筆抓 22:14→22:40」）。起點語意上本就模糊、時間窗也可能夾進
   無關討論，所以這是**事後可校正的 FYI**，使用者覺得偏了隨時可調。

**指標怎麼讀**（別過度解讀）：來回次數是最誠實的摩擦訊號；token 受 span 長度與
cache 影響大，當輔助看。三者並陳才有意義 —— 「3 來回就解掉」與「11 來回、40 分鐘」
是兩種故事。時間窗夾進的無關討論會灌進數字，解讀時心裡有數。

---

## 收尾整合 review（工作單元級；規劃內的 iteration 都做完、準備交付整個單元時）

切小刀讓每次 review 認知負擔低，但有個**結構性盲點**：每刀的 review 都是局部的，沒有
任何一步檢查「**整合後的整體**」。所以在宣告工作單元可交付前，做一次**整體** review，
兩個 lens：

- **完整性（vs plan / requirements）**：把整個工作單元的累積改動重新對照當初的計劃，
  **逐項**確認是否完整交付；落差**不論是否合理都列出**。per-iteration review 看不到
  「跨刀之後整體還缺什麼」（典型：散落的 doc / 註解沒跟著最終設計收斂）。
- **整合衛生（vs base branch）**：對 base branch 看**累積** diff，揪「中間 commit 改了
  又改回、淨值≈0 卻留下痕跡」的殘留（多餘的註解 / 格式 / 命名 / migration 疤痕）。意圖
  與 base 相同就該真的是 0，而不是留疤——對會 squash-merge 的 branch 尤其重要，最終
  diff 就是交付物本身。

**收尾 review 的發現＝一個新的（收尾）iteration**：它改的是已封板的範疇，依「回頭改
已通過的階段 = 新 iteration」（見 Phase 2）框成 `iteration_N`、走完整流程（盤點 → 一起
做 → 一起 review → 一次交付），而**不是散裝 cleanup commit**。這樣才誠實反映「原計劃
漏了什麼」。

（通常由 AI 在「規劃內的 iteration 都做完」時主動提議；使用者也可直接要求。完成後再進
Phase 4 retrospective。）

---

## Phase 4 — Retrospective（`retro` 或使用者要求）

iteration 結束、使用者 review 完後執行。

1. **`retrospectives/iterations.md`** — 補上這個 iteration 的 **outcome 敘事**：做了
   什麼、結果如何、與上一個 iteration 的關係。要有段落感、有承接，不是流水帳。
2. **`retrospectives/conversations.md`** — 確認 Phase 3 過程中該記的問題都進表了。
3. **蒸餾原則 → `mini-sprints/CLAUDE.md`**：回顧本工作單元 `conversations.md` 累積的
   問題，提煉出可複用原則，更新進**跨工作單元的** `mini-sprints/CLAUDE.md`，同時
   更新「當前進度」（指明工作單元）與「當前階段參考文件」。**只在 `retro` 或使用者
   明確說「更新 CLAUDE.md」時做這步。**

   蒸餾的紀律 —— **靠 conversations.md 的欄位判斷，不靠記憶**：

   - **用信心/復發升級階梯決定份量，不靠臨場感覺。**
     - `信心=暫定`（單案）→ **不升格**，留在 log。過早一般化只會堆雜訊原則。
     - `信心=確立`（同類再現過 / 已驗證）→ 提煉成原則，寫進 `CLAUDE.md`。
     - 多次復發（`復發=確認，第 3 次`以上）→ 升為**鐵則**，措辭加重、放醒目處。
     蒸餾前先掃 log：把同根因的多筆合併成**一條上拉的通則**，而不是各立窄規。
   - **更新欄位回填。** 蒸餾時若發現某筆從暫定變確立（這次又出現了），回去把該筆
     的 `信心`/`復發` 欄更新 —— log 要反映最新的二階狀態。
   - **釐清責任歸屬。** 依 `責任` 欄分流成兩類，寫進 `CLAUDE.md` 對應段落：
     - **對使用者的建議** —— 例如「需求討論時先確認 X 再交給 AI」。
     - **對 AI 的原則** —— 例如「動 X 模組前務必先讀 Y」。
     讓後續 session 雙方都能改進。
   - **什麼該回饋進 mini-sprints skill：只有「工作流本身的結構契約」。** 蒸餾的原則預設落在
     `mini-sprints/CLAUDE.md`（專案 / 個人層級）；要再升進 skill，須**同時**滿足兩關，否則
     歸到括號內的家：
     1. **屬流程結構**——關於迭代工作流的*結構*（iteration 邊界、階段交界紀律、收尾 review、
        retrospective 機制…）。「夠通用」不是進場券：通用但非流程結構的（某類 Go 寫法、通用
        測試 / 安全實務…）應**自成或歸入別的 team skill**；綁特定 repo 的歸**該 repo 的 rule-set**。
     2. **是契約、不是落實方式**——skill 只定義工作流*該長什麼樣*，不規定*怎麼落實*。「code 要被
        review」「要有測試」是契約；「固定派 subagent 自我 review」「先寫測試再實作」是落實方式
        （→ **個人 CLAUDE.md**）。
     兩關皆過才提議改 skill 本身。

### retrospectives/conversations.md 模板

這份是**物件層案例帳本**，餵養 Phase 4 對 `CLAUDE.md` 的蒸餾。每筆走
「偏差 → 根因 → 歸納原則」。設計刻意讓「該不該升格成原則」變成**有資料可查**，
而不是靠臨場記憶判斷。

```markdown
# Conversation Log

記錄導致實作方向轉折或效率損失的事件。良性的探索性討論（架構取捨、追問）不記。
復發欄是二階訊號：同類再現代表某個機制漏了，蒸餾時要升級該原則的份量。
信心：暫定（單案）／確立（同類再現或已驗證）。

| Iteration | 來源  | 說明  | 根因  | 責任  | 信心 | 復發  | 歸納原則（寫去哪）   |
|-----------|------|------|------|------|------|------|--------------------|
```

欄位定義：

- **來源** — 事件如何浮現：`使用者糾正` / `使用者提問→改進` / `重新設計` /
  `AI 自檢`。把「AI 自己抓到」也納入 —— log 不只記「人抓 AI」。並在格內標明這筆屬
  **轉折**（導致重工）還是**阻礙**（卡住、效率低落），兩類後續處理不同。
- **說明** — 視類別而定：
  - **轉折類**寫**偏差（AI 做的 → 應該的）**：AI 實際產出 vs 應有的樣子，雙邊都記，
    根因分析才有素材。
  - **阻礙類**寫**卡點 + 代價**：卡在什麼，加上三項指標「卡了 N 來回 / M 分鐘 /
    ~K 新增 token」。粗略紀錄即可；要精準時用「§3 測量阻礙的代價」流程取得實數。
- **根因** — **為什麼**會偏，不是發生什麼。要可抽象（例：「把單一規則過度套用、
  未分辨例外」），而非個案描述。
- **責任** — `使用者` / `AI` / `兩者`。供 Phase 4 分流成「對使用者的建議」與
  「對 AI 的原則」。
- **信心** — `暫定`（只出現一次）/ `確立`（同類再現過，或已被驗證）。
- **復發** — `否` / `近似（第 N 例）` / `確認（第 N 次）`。這是判斷升格的核心訊號。
- **歸納原則（寫去哪）** — 提煉出的可複用原則，**並標明它最後寫進哪裡**
  （`CLAUDE.md` 的哪段、或 spec 的哪節）。閉環，讓原則有明確的家。

### retrospectives/iterations.md 模板

```markdown
# Iteration History

## Iteration 1 — <date>
**Focus:** ...
**Outcome:** ...
**Key decisions:** ...
**承接上次:** <與前一 iteration 的關係；iteration 1 寫「起點」>

---
```

### retrospectives/reflections.md 模板

```markdown
# Reflections

跨 iteration 的模式、反覆出現的問題、要帶往後續的流程改進。
```

### mini-sprints/CLAUDE.md 模板

這份**跨工作單元**，是給下一個 session 的 AI 看的 briefing，不是給人看的歷史。
要短、可執行。蒸餾原則跨工作單元累積；當前進度必須指明**現在在哪個工作單元**。

```markdown
# mini-sprints — AI working state

## 當前進度
- 當前工作單元：<UNIT>，在 iteration N。已完成：... 待 review：... 待實作：...
- （其他工作單元的狀態若仍活躍，列在此）

## 對 AI 的原則（從各工作單元 retrospective 蒸餾，僅限重複出現的問題）
- <動手前要先做的事 / 已知地雷>

## 對使用者的建議（從 retrospective 蒸餾）
- <讓需求討論與 review 更順的習慣>

## 當前階段參考文件
<!-- 只列「現在這個階段真正需要」的指標，隨階段切換時刻維護，不堆積。 -->
- 需求：<UNIT>/specs/requirements.md
- 歷史：<UNIT>/retrospectives/iterations.md
```

---

## 維護與自我演進（skill self-improve）

這個 skill 自己也要迭代。改善的**候選資格**已在 Phase 4 的「什麼該回饋進 mini-sprints
skill」定義（兩道閘：屬流程結構 + 是結構契約）——本節規範**確認候選之後，怎麼動 skill**。

**流程：**

1. **確認資格**——套 Phase 4 的兩道閘。不過關 → 歸別的 team skill / repo rule-set /
   個人工作區，**不動本 skill**（避免它變成什麼都收的雜物櫃）。
2. **先提案、不擅自改**——skill 是團隊共享物。把「改什麼、為什麼」攤給維護者確認後再動
   （同階段交界紀律）。
3. **改 `SKILL.md`，守精簡**——優先**改寫既有段落**而非疊加新段；**砍冗餘**與**加內容**同等
   重要；用語 / 結構與既有對齊。skill 越精簡越好用。
4. **實質改動才記一筆 `CHANGELOG.md`**——記：**改了什麼 / 為什麼（動機 + 觸發來源，最好
   連到那次 retrospective 案例）/ 影響的段落**。這是給未來維護者的脈絡：當 skill 變複雜，
   他們才查得到每段敘述是怎麼、為何被加進來的（含「曾加入又移除」這類決策）。
   **「實質」＝引入新概念、調整定義 / 流程、新增或移除段落。純清理對齊（typo、用詞統一、
   去重、排版）不引入新東西 → 不記，那是雜訊。**

**紀律：self-improve 不只加、也要減。** 定期回看有沒有可合併 / 可刪的段落；長期目標是
skill 保持精簡、每段都配得上它佔的篇幅。
