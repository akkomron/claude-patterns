# Changelog

What changed in the house style and the global config, when, and why. Every entry is timestamped; old entries are
never rewritten.

---

## 2026-10-14

### 16:16 (2026-10-14) — The house style as a plugin: the ai-project-patterns skill, a global CLAUDE.md, an installer

- `skills/ai-project-patterns/PATTERN.md`: the layout, living docs, CHANGELOG, commit and experiment rules, and a
  new-repo checklist. Examples are generic; plain result-first commit subjects are chosen over `feat:`/`fix:` prefixes.
- `skills/ai-project-patterns/SKILL.md`: when the skill applies; a repo's own conventions win.
- `skills/ai-project-patterns/templates/`: `registry.py` and `doc_toc.py`, the two files the checklist copies.
- `global/CLAUDE.md`: the always-on short form for `~/.claude/CLAUDE.md`.
- `install.sh`: symlinks into `~/.claude` so a `git pull` updates them; an existing file is backed up, never deleted.
- `.claude-plugin/`: plugin and marketplace manifests, so the skill installs with `/plugin`.
