# Global instructions

## House style for AI projects

The full playbook is `~/.claude/PATTERN.md` (also the `ai-project-patterns` skill): folder layout, living docs, CHANGELOG, commits and experiment discipline.
Read it before starting a new repo, scaffolding one, or adding a module, config, script or doc to an AI/ML project.
A repo's own CLAUDE.md, or a convention its history already shows, wins over this file.

Always, in my repos:

- **Commits**: one plain-English line, no `feat:`/`fix:` prefix, no trailing period, about 60–120 characters. Say the
  result, not the files, shaped `<Topic>: <what was done or found>`, with `;` between two related outcomes and the
  number when there is one. Examples: `Run 12 read; run 13 prepared: the tokenizer trained on our own text`,
  `The labelling app saved no answer since v2: two functions with the same name; fixed`. One logical change per commit.
- **CHANGELOG.md**: every commit adds an entry in the same commit, under `## YYYY-MM-DD`, as
  `### HH:MM (YYYY-MM-DD) — <the commit subject>` (newest on top). Bullets name the files, knobs, numbers and tests,
  and the doc section with the detail. For design decisions, also write What / Why / Rejected alternative / Left out of
  scope. Never rewrite an old entry; add a correcting one.
- **Docs**: one question per doc and one home per fact; other docs link instead of copying. The code, its test, its
  config and template knob, the affected docs and the CHANGELOG entry land together.
- **Layout**: the library in `src/<pkg>/` (registry-driven, no `if/elif` switchboards), thin CLIs in `scripts/`, one
  complete template per stage in `configs/templates/`, flat `tests/test_<module>.py`, `data/` and `experiments/`
  gitignored.
- **Experiments**: one variable per run, a named "vs." run, two seeds, a paired bootstrap, and never train on a benchmark.
- **Safety**: never delete data (move it to `_broken/`), and write files atomically (`.part`, then rename).
- Use absolute dates (YYYY-MM-DD) in every doc and commit.
