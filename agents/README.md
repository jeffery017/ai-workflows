# agents

Personal Claude Code subagents. Each agent is a single `.md` file here, symlinked
into `~/.claude/agents/` by `make link-all-agents`.

Add one as `agents/<name>.md` with frontmatter:

```markdown
---
name: <name>
description: When this subagent should be invoked.
tools: Read, Grep, Glob, Bash   # optional; omit to inherit all tools
model: sonnet                    # optional; inherit / opus / sonnet / haiku
---

<the agent's system prompt — role, workflow, boundaries>
```

Then run `make link-all-agents`. This `README.md` is ignored by the Makefile.
