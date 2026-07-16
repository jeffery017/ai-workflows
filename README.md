# personal-skills

Personal collection of Claude Code **skills** and **agents**. Each is symlinked into
`~/.claude/` so it's available globally in Claude Code.

## Install

```bash
git clone <this-repo> ~/personal-skills
make -C ~/personal-skills link-all          # link all skills + agents
make -C ~/personal-skills help              # list all targets
make -C ~/personal-skills link-all-skills   # just the skills
make -C ~/personal-skills link-all-agents   # just the agents
```

Skills are symlinked into `~/.claude/skills/`, agents into `~/.claude/agents/`. If a
target name already exists as a real file/dir (not a symlink), it's left untouched and
a warning is printed. `make link-all` is idempotent — re-running is safe, and after a
`git pull` you don't strictly need to re-run since symlinks point at the live repo.

## Layout

```
personal-skills/
├── skills/<name>/SKILL.md   # each skill is a directory (+ optional references/, scripts/)
├── agents/<name>.md         # each agent is a single .md file
├── .claude/skills/          # repo-private skill for maintaining this repo (not linked out)
├── Makefile
└── README.md
```

The Makefile discovers content by location: skills from `skills/*/SKILL.md`, agents from
`agents/*.md` (excluding `agents/README.md`). Put files in the right place and they're
picked up automatically — no Makefile edits needed.

## Skills

| Skill | Trigger | Description |
|-------|---------|-------------|
| [code-walkthrough](skills/code-walkthrough/SKILL.md) | 「帶我了解這段流程」/ "walk me through X" | Guided narrative tour of existing code along one real execution path. |
| [mini-sprints](skills/mini-sprints/SKILL.md) | `/mini-sprints` /「規劃這個 ticket / 這份 plan」「規劃下一個 iteration」 | Iterative dev workflow: split one work unit's requirement→design→implementation into deliberately narrow mini-sprints. |

## Agents

| Agent | When invoked | Description |
|-------|--------------|-------------|
| _(none yet)_ | | |

## Adding a skill

1. Create `skills/<name>/SKILL.md` with `name` + `description` frontmatter.
2. Add a row to the **Skills** table above.
3. `make link-all-skills`.

## Adding an agent

1. Create `agents/<name>.md` with `name` + `description` frontmatter (see [agents/README.md](agents/README.md)).
2. Add a row to the **Agents** table above.
3. `make link-all-agents`.

> Working inside this repo, the private `repo-maintainer` skill (in `.claude/skills/`)
> walks Claude through all of the above and keeps things in sync.
