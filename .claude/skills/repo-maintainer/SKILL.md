---
name: repo-maintainer
description: >-
  Maintain THIS repo (personal-skills) — the personal collection of Claude Code
  skills and agents. Use whenever the user wants to add, rename, remove, or edit a
  skill or an agent in this repo, or asks to keep its README / Makefile / structure
  in sync. Triggers on 「新增一個 skill」「加一個 agent」「整理這個 repo」
  "add a skill here", "create an agent", "register it", "update the README table".
  Does NOT apply to skills/agents in other repos.
---

# personal-skills repo maintainer

這個 repo 是個人版的 Claude Code skill / agent 集合。它透過 symlink 把內容掛進
`~/.claude/skills/` 和 `~/.claude/agents/`，讓 Claude Code 全域可用。維護時請守住下面的結構與流程。

## 結構（不變式）

```
personal-skills/
├── skills/<name>/SKILL.md   # 每個 skill 是一個目錄，內含 SKILL.md（+ 可選 references/、scripts/）
├── agents/<name>.md         # 每個 agent 是單一 .md 檔
├── .claude/skills/          # 這個 repo 私有的維護 skill（就是本檔），不對外 link
├── Makefile                 # link 全部到 ~/.claude/{skills,agents}/
└── README.md                # 含 skills / agents 兩張總表，需與實際內容同步
```

Makefile 靠檔案位置自動發現內容：skills 來自 `skills/*/SKILL.md`，agents 來自 `agents/*.md`
（會排除 `agents/README.md`）。**放對位置 = 自動被發現**，不必改 Makefile。

## 新增一個 skill

1. 建 `skills/<name>/SKILL.md`，frontmatter 至少要有：
   ```markdown
   ---
   name: <name>
   description: >-
     一段話描述「Claude 何時該啟用這個 skill」——寫清楚觸發情境與關鍵詞，這是觸發準確度的關鍵。
   ---
   ```
2. 需要時加 `references/*.md`（Claude 載入的背景文件）、`scripts/`（可執行輔助）。
3. 在 README 的 **Skills** 表加一列。
4. `make link-all-skills`（或 `make link-<name>-skill`）。

## 新增一個 agent

1. 建 `agents/<name>.md`，frontmatter：
   ```markdown
   ---
   name: <name>
   description: When this subagent should be invoked.
   tools: Read, Grep, Glob, Bash   # 可選；省略則繼承全部工具
   model: sonnet                    # 可選；inherit / opus / sonnet / haiku
   ---

   <agent 的 system prompt — 角色、流程、邊界>
   ```
2. 在 README 的 **Agents** 表加一列。
3. `make link-all-agents`（或 `make link-<name>-agent`）。

## 重新命名 / 刪除

- 用 `git mv` 搬移以保留歷史。
- 改名或搬移後，`~/.claude/` 裡的舊 symlink 會變成 dangling，需手動清掉舊連結再 `make link-all`。
- 刪除：移掉目錄/檔案、移除 README 對應列、刪掉 `~/.claude/{skills,agents}/` 裡的 symlink。

## 完成前的檢查

- README 的兩張表與 `skills/`、`agents/` 實際內容一致。
- frontmatter 的 `name` 與目錄/檔名一致。
- 跑過 `make link-all`，確認輸出沒有非預期的 `⚠️ skipped`（代表該名稱已有非 symlink 的本機版本）。
- 列出 `~/.claude/skills/` 與 `~/.claude/agents/` 確認沒有 dangling symlink。
