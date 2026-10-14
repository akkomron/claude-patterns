# claude-patterns

A house style for AI/ML research repositories, packaged as a Claude Code plugin (the `ai-project-patterns` skill),
plus a global `CLAUDE.md` that applies it in every session.

| Path | What it is |
|---|---|
| `skills/ai-project-patterns/SKILL.md` | The skill's entry point: when it applies and how |
| `skills/ai-project-patterns/PATTERN.md` | The full playbook: layout, living docs, CHANGELOG, commits, experiments, new-repo checklist |
| `skills/ai-project-patterns/templates/` | `registry.py` (name → class registry) and `doc_toc.py` (contents blocks for long docs) |
| `global/CLAUDE.md` | The always-on short form, for `~/.claude/CLAUDE.md` |
| `install.sh` | Links `global/CLAUDE.md`, `PATTERN.md` and the skill into `~/.claude` |
| `.claude-plugin/` | Plugin and marketplace manifests |

## Install

**As a plugin (the skill only), in Claude Code:**

```
/plugin marketplace add akkomron/claude-patterns
/plugin install ai-project-patterns@akkomron-plugins
```

**Everything, including the global CLAUDE.md (your own computers):**

```bash
git clone https://github.com/akkomron/claude-patterns ~/Projects/claude-patterns
bash ~/Projects/claude-patterns/install.sh
```

`install.sh` symlinks the files, so `git pull` updates them in place. If a file is already at the target path, it is
moved to `<name>.bak-<date>`, not deleted.

## Change the style

Edit `PATTERN.md` (and `global/CLAUDE.md` when an always-on rule changes). Commit in the style of PATTERN.md §5, add a
CHANGELOG entry, and bump `version` in `.claude-plugin/plugin.json` so that plugin users get the update.
