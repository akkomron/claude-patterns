---
name: ai-project-patterns
description: House style for AI/ML research repositories. Use when starting or scaffolding a new AI/ML project; when adding a module, config, training/eval script, test or doc to one; when planning or recording an experiment; and when writing a commit message or CHANGELOG entry. Covers folder layout (src/ library, configs/templates, thin scripts/), living docs with one home per fact, a timestamped CHANGELOG, plain-English result-first commits, and one-variable-per-run experiment discipline.
---

# AI project patterns

Read [PATTERN.md](PATTERN.md) before acting; it is the full playbook. The two files its §7 checklist copies are
[templates/registry.py](templates/registry.py) and [templates/doc_toc.py](templates/doc_toc.py)
(at `${CLAUDE_SKILL_DIR}/templates/`).

How to apply it:

1. **A repo's own conventions win.** If the repo has its own CLAUDE.md or its git history shows a different commit or
   docs style, follow that, and use PATTERN.md only where the repo is silent.
2. **New repo**: walk PATTERN.md §7 step by step. Make the first commit in the §5 style.
3. **Changing an existing repo**: put the code, its test, the new config knob (in the template too), the docs it
   touches (§3) and a CHANGELOG entry (§4) into the same commit.
4. **Commit message**: one plain-English line saying the result, shaped `<Topic>: <what was done or found>`, with no
   `feat:`/`fix:` prefix (§5). The CHANGELOG heading is the same sentence.
5. **Experiments**: before launching a run, write down its question and the run it is compared against, and add a run
   ledger line (§3, §6).
