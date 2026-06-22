# team-skills

Shared Claude Code skills for the Dragonfly team.

## Install

```bash
git clone <this-repo> ~/team-skills
make -C ~/team-skills link-all-skills      # link all skills
make -C ~/team-skills help                 # list all targets
make -C ~/team-skills link-jira-skill      # link just one skill
```

Each skill is symlinked into `~/.claude/skills/`. If you already have a personal skill with the same name (a real directory, not a symlink), it is left untouched and a warning is printed. `make link-all-skills` is idempotent — re-running is safe, and after a `git pull` you don't strictly need to re-run since the symlinks point at the live repo directory.

## Skills

| Skill | Trigger | Description |
|-------|---------|-------------|

## Adding a new skill

1. Create a subdirectory: `team-skills/<skill-name>/`
2. Add a `SKILL.md` with the required frontmatter:
   ```markdown
   ---
   name: skill-name
   description: >
     One paragraph describing when Claude should activate this skill.
   ---
   ```
3. Optionally add `references/` (markdown docs) and `scripts/` (helper scripts)
4. Run `make link-all-skills` again — it picks up any new subdirectory automatically (the Makefile discovers skills via `*/SKILL.md`)

## Structure of a skill

```
skill-name/
├── SKILL.md          # Required — frontmatter + instructions for Claude
├── references/       # Optional — markdown docs Claude loads for context
│   └── *.md
└── scripts/          # Optional — helper scripts Claude can run
    └── *.py
```
