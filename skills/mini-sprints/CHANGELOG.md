# mini-sprints — Changelog

記錄 skill 每次改善的「改了什麼 / 為什麼 / 影響段落」。維護方式見 `SKILL.md` 的
「維護與自我演進」。最新在上；日期為 skill 改動日。

## 2026-07-16 — 新增兩條約束：架構先行、小任務豁免
**改了什麼：** Phase 1 漸進式段新增「漸進式只放寬需求細節、不放寬整體架構」——拆 scope
前必須先有整體架構與流程的設計掌握（需要時落成 `design.md`）。Phase 2 新增「任務夠小就
別硬拆」，範圍單純時允許一個 iteration 完成。
**為什麼：** 防止「漸進式」被誤讀成兩種極端：一是只顧眼前細部 scope、缺整體架構骨架，
各刀難整合；二是連單純小任務也硬套多刀切割的儀式。兩條把 skill 的適用邊界講清楚。
**影響段落：** Phase 1「漸進式定義需求」；Phase 2「目標」後。
**來源：** 使用者提出的兩條約束。

## 2026-07-16 — 三件套對齊：新增 README.md、SKILL.md 瘦身
**改了什麼：** 新增 `README.md`（給人的設計說明：動機 / 瀑布式痛點 / 檔案結構取捨 / 演進
脈絡；含一個跑到一半的工作單元範例目錄樹，讓人感受實際長相）。SKILL.md「為什麼存在」段重寫為精簡的「核心心法」，把展開的問題論述與設計取捨移到
README，避免與 README 重複；各 Phase 內驅動判斷的 why 保留。
**為什麼：** repo-maintainer 新增「skill 三件套」不變式（README.md / CHANGELOG.md /
SKILL.md 內 self-improve 段），要求 README 給人、SKILL 給 Claude、受眾不同不混寫。
mini-sprints 原本缺 README，且設計動機混在 SKILL.md。
**影響段落：** 新增 `README.md`；SKILL.md「為什麼存在」→「核心心法」；Phase 1「漸進式
定義需求」段去重（刪與核心心法重複的「整體需求可模糊、scope 要清晰」）並拆掉論證瀑布式
痛點的辯護句（已入 README）。
**來源：** 使用者要求依 repo-maintainer 新規則 review mini-sprints。

## 2026-06-25 — 自我演進機制標準化
**改了什麼：** `SKILL.md` 新增「維護與自我演進（skill self-improve）」章節；新增本
`CHANGELOG.md`。並定義 CHANGELOG 紀錄紀律：**只記實質改動**（新概念 / 定義 / 流程變更、
增刪段落），純清理對齊（typo、用詞統一、去重、排版）不記。
**為什麼：** 先前已定義「什麼 insight 該納入 skill 改善候選」（Phase 4 兩道閘），但沒規範
「確認候選後**怎麼動 skill**、怎麼留下脈絡」。標準化更新流程 + 變更紀錄，讓 skill 日後變
複雜時，維護者查得到每段敘述的來由。
**影響段落：** 新增「維護與自我演進」段；新增 `CHANGELOG.md`。
**來源：** 使用者要求把 self-improve 流程標準化。

## 2026-06-25 — 首次實跑（flight-anchored-issues）後的 retrospective 反饋
第一個跑完整生命週期的工作單元；retrospective 蒸餾出數條對「工作流本身」的改善。

- **去 Jira 化：「ticket」→「工作單元（work unit）」。** 動機：首跑就**沒有 Jira ticket**、
  context 來自 plan 文件，但原 skill 從 description 到模板都把 Jira 當前提。Jira 降為三種
  context 來源之一（Jira / plan 文件 / 純討論）。影響：frontmatter、標題、為什麼存在、檔案
  結構、啟動步驟 3、Phase 1 步驟 1、requirements.md 模板（`## Jira Ticket` → `## 來源`）。
- **新增「收尾整合 review」段。** 動機：切小刀有結構盲點——每刀 review 都是局部的，沒有
  任何一步看「整合後的整體」；首跑靠使用者手動引入「兩視角 review」（完整性 vs plan、整合
  衛生 vs base branch）才抓到 plan 漏做 + migration「+1−1」殘留。明定其發現＝新的收尾
  iteration。影響：Phase 3 與 Phase 4 之間新增整節。
- **Phase 3 §1 一般化為「一刀一次交付」。** 動機：首跑把收尾修正**散裝 commit**被使用者
  糾正；原 §1 只談「消化使用者回饋」，未涵蓋「自己的修正批次也要整批一起交付」。git commit
  顆粒度屬個人，留個人 CLAUDE.md。
- **Phase 4 新增「什麼該回饋進 skill」的候選資格判準（兩道閘）。** 動機：要讓 self-improve
  有明確進場門檻。閘①屬流程結構（通用性不是進場券；通用但非流程結構 → 別的 team skill、
  綁 repo → repo rule-set）；閘②是結構契約而非落實方式（落實方式 → 個人 CLAUDE.md）。此
  判準經三輪收緊定稿。
- **（加入又移除）Phase 2「切法先驗證耦合」。** 一度加進 Phase 2，後依上述兩道閘判定它屬
  「怎麼 plan」的個人落實方式（非工作流結構），移除、改歸個人 CLAUDE.md。記此決策以示
  「候選被考慮後也可能被拒」——這正是 changelog 要保存的脈絡。

**來源：** flight-anchored-issues 的 retrospectives/{conversations,iterations,reflections}.md。

## （初始）— skill 建立
mini-sprints skill 初版：四階段（Requirements / Iteration Planning / Implementation /
Retrospective）+ 檔案結構（specs / iteration_N / retrospectives）+ conversations.md 的
信心 / 復發升級階梯與 CLAUDE.md 蒸餾機制。詳細沿革見 git history
（commits `add mini-sprints`、`update mini-sprints`）。
