SKILLS_DIR    ?= $(HOME)/.claude/skills
REPO_DIR      := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
SKILLS        := $(sort $(notdir $(patsubst %/SKILL.md,%,$(wildcard $(REPO_DIR)/*/SKILL.md))))
LINK_TARGETS  := $(addprefix link-,$(addsuffix -skill,$(SKILLS)))

.PHONY: help link-all-skills $(LINK_TARGETS)

help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  help              Show this help"
	@echo "  link-all-skills   Link all skills (symlink into $(SKILLS_DIR))"
	@echo ""
	@echo "Skills (run 'make link-<name>-skill' to link one):"
	@for s in $(SKILLS); do printf "  link-%s-skill\n" "$$s"; done
	@echo ""
	@echo "Variables:"
	@echo "  SKILLS_DIR        Target dir (default: \$$HOME/.claude/skills)"

link-all-skills: $(LINK_TARGETS)

$(LINK_TARGETS): link-%-skill:
	@mkdir -p $(SKILLS_DIR)
	@name="$*"; target="$(SKILLS_DIR)/$$name"; src="$(REPO_DIR)/$$name"; \
	if [ -e "$$target" ] && [ ! -L "$$target" ]; then \
	  echo "⚠️  skipped $$name — personal version exists at $$target"; \
	else \
	  ln -sfn "$$src" "$$target"; \
	  echo "✅ linked $$name"; \
	fi
