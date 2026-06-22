SKILLS_DIR    ?= $(HOME)/.claude/skills
AGENTS_DIR    ?= $(HOME)/.claude/agents
REPO_DIR      := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))

SKILLS        := $(sort $(notdir $(patsubst %/SKILL.md,%,$(wildcard $(REPO_DIR)/skills/*/SKILL.md))))
AGENTS        := $(sort $(notdir $(basename $(filter-out %/README.md,$(wildcard $(REPO_DIR)/agents/*.md)))))

LINK_SKILL_TARGETS := $(addprefix link-,$(addsuffix -skill,$(SKILLS)))
LINK_AGENT_TARGETS := $(addprefix link-,$(addsuffix -agent,$(AGENTS)))

.PHONY: help link-all link-all-skills link-all-agents $(LINK_SKILL_TARGETS) $(LINK_AGENT_TARGETS)

help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  help              Show this help"
	@echo "  link-all          Link all skills and agents"
	@echo "  link-all-skills   Link all skills (symlink into $(SKILLS_DIR))"
	@echo "  link-all-agents   Link all agents (symlink into $(AGENTS_DIR))"
	@echo ""
	@echo "Skills (run 'make link-<name>-skill' to link one):"
	@for s in $(SKILLS); do printf "  link-%s-skill\n" "$$s"; done
	@echo ""
	@echo "Agents (run 'make link-<name>-agent' to link one):"
	@for a in $(AGENTS); do printf "  link-%s-agent\n" "$$a"; done
	@echo ""
	@echo "Variables:"
	@echo "  SKILLS_DIR        Target dir (default: \$$HOME/.claude/skills)"
	@echo "  AGENTS_DIR        Target dir (default: \$$HOME/.claude/agents)"

link-all: link-all-skills link-all-agents

link-all-skills: $(LINK_SKILL_TARGETS)

link-all-agents: $(LINK_AGENT_TARGETS)

$(LINK_SKILL_TARGETS): link-%-skill:
	@mkdir -p $(SKILLS_DIR)
	@name="$*"; target="$(SKILLS_DIR)/$$name"; src="$(REPO_DIR)/skills/$$name"; \
	if [ -e "$$target" ] && [ ! -L "$$target" ]; then \
	  echo "⚠️  skipped skill $$name — non-symlink exists at $$target"; \
	else \
	  ln -sfn "$$src" "$$target"; \
	  echo "✅ linked skill $$name"; \
	fi

$(LINK_AGENT_TARGETS): link-%-agent:
	@mkdir -p $(AGENTS_DIR)
	@name="$*"; target="$(AGENTS_DIR)/$$name.md"; src="$(REPO_DIR)/agents/$$name.md"; \
	if [ -e "$$target" ] && [ ! -L "$$target" ]; then \
	  echo "⚠️  skipped agent $$name — non-symlink exists at $$target"; \
	else \
	  ln -sfn "$$src" "$$target"; \
	  echo "✅ linked agent $$name"; \
	fi
