# PATTERN — how an AI project repo is laid out, documented and committed

A house style for AI/ML research repositories, distilled from several hundred commits of a long-running research
project. Follow it in every new AI project, whatever the domain (vision, speech, NLP, tabular, RL). The bundled
`templates/` folder (next to this file) holds the two files the checklist in §7 copies.

Contents: [1 Layout](#1-folder-layout) · [2 Code](#2-code-idioms) · [3 Docs](#3-docs-one-question-per-file-one-home-per-fact)
· [4 CHANGELOG](#4-changelogmd) · [5 Commits](#5-commit-messages) · [6 Experiments](#6-experiment-discipline)
· [7 New repo checklist](#7-starting-a-new-repo-checklist)

---

## 1. Folder layout

```
<repo>/
  README.md              premise, dated status checklist, layout tree, docs map, "where a fact lives" table, setup
  CHANGELOG.md           chronological, timestamped, never rewritten (§4)
  pyproject.toml         src layout, minimal deps, each dep commented with why and when it was added
  .gitignore             every entry commented; data/ and experiments/ always ignored
  .gitattributes         *.sh text eol=lf
  src/<pkg>/             the importable library (pip install -e ".[dev]")
    core/                registry.py (name -> class), protocols.py (typing.Protocol contracts), config.py (yaml -> dataclass)
    <concern>.py         one module per concern: data, manifest, transforms, models/encoders, tasks/heads, losses, decode
    evaluation/          metrics.py, significance.py (paired bootstrap)
    training/            loop.py + one module per training stage
    <subsystem>/         a self-contained subpackage for a separate stage or route; the core never imports it
  configs/
    templates/           ONE complete template per stage, every knob at its default: "copy, change one thing, rename"
    <stage>/             one yaml per run; file name == `name:` == checkpoint name; seeds `_s43`, folds `_cv0`..`_cv4`
    release/             frozen release candidates (rc1, rc2, ...), header comment: what changed + measured numbers
  scripts/
    train/               one entry point per stage, named like its config folder (train/stage0_x.py <-> configs/stage0_x/)
    data/                download, extract, audit, build manifests; one job per script
    eval/                predict, compare, sweep, report; <topic>_server.sh batch runners for the GPU host
    demo/                small apps (+ static/ html)
    tools/               doc_toc.py, server status, exports
    tracking/            MLflow import/sync
  tests/                 flat, test_<module>.py, pytest; tests also guard configs and templates
  docs/                  the living documents (§3)
  data/                  local dataset copies (gitignored)
  experiments/           checkpoints, mlflow.db, predictions, logs (gitignored)
```

Rules:
- Library code lives only in `src/<pkg>/`. Scripts are thin CLIs that import it, and no logic is duplicated in a script.
- Build an abstraction only when a second real implementation needs it (Rule of Three). Say so in the module docstring.
- Components register themselves by name, and configs pick them by string. There is no central `if/elif` switchboard:
  ```python
  @BACKBONES.register("transformer_small")
  class SmallTransformer(nn.Module): ...

  model = BACKBONES.build(config["backbone"], **config["backbone_args"])
  ```
- Keep dependencies minimal: only what committed code imports. Feature-only deps go in `[project.optional-dependencies]`.
- Set the Python floor from the real runtime host (e.g. 3.9) and keep `from __future__ import annotations` in every module.

## 2. Code idioms

- **A module docstring explains the problem, not the code.** It says what the module solves, why it is no bigger, which
  doc section it implements (`docs/research/x.md §6`), and the measured numbers behind every threshold ("beyond the
  99.99th percentile: 0.79").
- **Scripts**: the docstring opens with copy-pasteable usage lines. Use `argparse.ArgumentParser(description=__doc__,
  formatter_class=argparse.RawDescriptionHelpFormatter)`, then `def main() -> None` and `if __name__ == "__main__":`.
- **Never destroy data.** Move bad files to `_broken/` instead of deleting them. Write atomically: write `<name>.part`,
  then rename it. Back up anything people annotate, on a schedule.
- **Tests**: the module docstring is one line stating the behaviour it guards ("a file cut short is moved aside, never
  deleted"). Use `tmp_path`, and test scripts end to end through `subprocess`. One test fails when a config lacks a knob
  that its template has.
- **Server batch scripts** (`scripts/eval/<topic>_server.sh`) start with a header comment saying which question each
  run answers and what it is compared against, plus the exact launch line:
  `tmux new -d -s <name> '... | tee experiments/logs/<name>.log'`. Then come `set -euo pipefail`,
  `cd "$(dirname "$0")/../.."`, a preflight check that the code the script needs is present, and
  `echo "== <step> $(date +%H:%M)"` between stages.
- Comments explain *why*, at the end of the line: `MAX_LEN = 512  # the 99.9th percentile of training lengths`.
- In a config yaml, group fields under `# ---- input / architecture / data / training` rulers, spell out every field,
  and add a `notes:` field saying what the run tests.

## 3. Docs: one question per file, one home per fact

Each doc answers exactly one question. A fact lives in one doc only. Other docs link to it (`DATA.md §3b`) instead of
copying it. The README holds both maps: "Document | Answers" and "Question | Home".

| File | Answers | Kept how |
|---|---|---|
| `README.md` | What is this, where does it stand, where is everything? | status list, each line dated, ✅ / ⚠️ / ➡️ |
| `CHANGELOG.md` | What changed, when, why, and what was rejected? | append-only, never rewritten |
| `docs/ARCHITECTURE.md` | What does the code look like *right now*? | **overwritten** on every module or knob change; ends with an "Update policy" |
| `docs/DATA.md` | What data do we have, and what did the audits find? | a corpus registry: size, licence, access, path, status |
| `docs/EXPERIMENTS.md` | What did we run, what did it show, what is next? | Scoreboard · Run ledger · Tried · Learned · To try |
| `docs/HYPOTHESES.md` | Which questions are still open? | `[H1]`, `[H2]`…; priority matrix; settled ones move to "Resolved" |
| `docs/STRATEGY.md` | In what order do we pursue them, and what result moves us on? | newest section on top (`0000.`, `000.`, `00.`), marked "read this first" |
| `docs/<FOCUS>.md` | The current main problem, in depth | one file per major route |
| `docs/analysis/<YYYY-MM-DD>/` | A dated data analysis | README.md + `figN_*.png` |
| `docs/research/README.md` | Who else works on this, and what did they reach? | field map |
| `docs/research/literature/<slug>.md` | What a paper says, and what it means for us | + `pdf/<slug>.pdf`; an index table with status (📄 full text / 🔍 summary) |
| `docs/presentations/<YYYY-MM-DD>_<name>` | What we tell stakeholders, with a source for every claim | dated |

Formats:
- **Run ledger** (EXPERIMENTS): `| # | Date | Run | Question | vs. | Answer | Recorded in |`, one line per run, marked
  ✅ answered · ❌ invalid run · ⏳ planned.
- **Hypothesis entry**: an `<a id="h36"></a>` anchor, then `### [H36] <the claim as a sentence>`, followed by
  **Status:** (✅ / ❌ refuted / ➖ partly / open, with numbers), **Source of the idea:** and **What would settle it:**.
- **Long docs** get a generated contents block between `<!-- toc:start -->` and `<!-- toc:end -->`, written by
  `python scripts/tools/doc_toc.py` and never edited by hand.
- Each living doc opens with what it is for and how it differs from its neighbours, then a "Related documents" line.
- Use absolute dates (`2026-10-14`), section signs (`§5c`), run numbers and H-ids, so cross-links stay exact.
- **Same commit, same session**: the code, its test, its config and template knob, the docs it touches and the
  CHANGELOG entry land together.

## 4. CHANGELOG.md

The header says what the file records (what, in which file, why, and which alternative was rejected), that every entry
is timestamped, and the reference style (`project/file:line`).

Routine entry (compact form):

```markdown
## 2026-10-14

### 14:35 (2026-10-14) — Balance by source: the sampler draws each class from different users first

- `BalancedSampler(by="user")` (config `sample_by_user`): a class's k samples from k different users first. The new
  knob spelt out in every training config and the template.
- Twin: `base_byuser` (vs. run 86); `scripts/eval/balance_server.sh`. `tests/test_balance.py`.
  research/data_methods.md §2.5.
```

Design-decision entry (long form):

```markdown
### 11:15 (2026-10-14) — `src/<pkg>/core/protocols.py`: the `Backbone` protocol

**What:** ...
**Why `Protocol`, not `ABC`:** ...
**Rejected alternative:** ...
**Left out of scope (for now):** ... (Rule of Three)
**Literature connection:** ...
```

- The newest day goes on top, and within a day the newest entry goes on top. Take the time from `date +%H:%M`.
- The heading is the same sentence as the commit subject.
- Bullets name the files, functions and config knobs touched, the numbers measured (`0.525 -> 0.225`), the tests added,
  and the doc section that holds the detail.
- Corrections never edit an old entry. A new entry says what the old one got wrong.

## 5. Commit messages

Conventional-commit prefixes (`feat:` / `fix:` / `doc:`) are deliberately not used: the subject itself says what
happened.

- **One line.** No type prefix, no trailing period, about 60–120 characters. Add a body only when a list adds something
  (usually the docs updated, as `- ` bullets).
- **Say the result, not the files.** Write plain English for someone reading `git log` a month later.
- Shape: `<Topic>: <what was done or found>`. Join two related outcomes with `;`.
- Include the number when there is one.
- Experiment work moves through these status words: **prepared** (configs and scripts ready) → **queued** → **built** →
  **read** (results analysed) → **released**. Also used: **researched, planned**, **audited**, **fixed**.
- A bug fix names the symptom and the cause: `The labelling app saved no answer since v2: two functions with the same name; fixed`.
- One commit per logical change, and it includes its CHANGELOG entry under the same title.

Examples:
```
Run 12 read; run 13 prepared: the tokenizer trained on our own text
rc2 read: +12% on new users, level on the benchmark
A power cut: checkpoints written whole, and a checker for the ones cut short
The field set is a benchmark only: every user tested, none trained
Balance measured: a class's real-world accuracy follows its number of users, not of samples
A quality score for every sample: researched, planned
Fix: the labelling app crashed at startup (an edit split its save loop); a smoke test
dedupe.py: a stricter threshold (0.8 merged near-duplicates that differ)
```

Avoid: `feat: add quality module`, `update docs`, `fix bug`, `WIP`.

## 6. Experiment discipline

- **One variable per run.** A new config is a copy of its template, or of the run it is compared against, with one
  change. A run that changes two things is marked confounded in the ledger and redone.
- Every run has a **question** and a **"vs."** run (its twin or control) before it starts.
- A result needs **two seeds** (42 and 43) before it counts. Judge a recipe on its mean, not its best seed.
- Test significance with a **paired bootstrap** on the same test items, and report the interval.
- **Never train on a benchmark**, and keep everyone in it out of training. Fix the split before anything is frozen.
- Measure the real world, not only the curated test. When it isn't measured yet, say so in the README status (⚠️).
- A release is a frozen config in `configs/release/` with its measured numbers in the header.
- Track every run locally (MLflow with sqlite under `experiments/`, no cloud). Import earlier or external runs and compare
  before launching a run that may repeat one.
- Write targets down with a date (e.g. "error rate <30% does no harm / <15% usable / <10% stretch").

## 7. Starting a new repo (checklist)

1. `git init`, then create the folders in §1 (empty folders get a `.gitkeep`).
2. `pyproject.toml`:
   ```toml
   [build-system]
   requires = ["setuptools>=64", "wheel"]
   build-backend = "setuptools.build_meta"

   [project]
   name = "<pkg>"
   version = "0.0.1"
   description = "<one line>"
   readme = "README.md"
   requires-python = ">=3.9"   # set by the runtime host; say which one and why
   # Kept minimal on purpose: only what the committed code imports. Each dep: why, and the date it was added.
   dependencies = []

   [project.optional-dependencies]
   dev = ["pytest>=7.0"]

   [tool.setuptools.packages.find]
   where = ["src"]

   [tool.pytest.ini_options]
   testpaths = ["tests"]
   ```
3. `.gitignore`, with a comment on every entry:
   ```gitignore
   __pycache__/
   *.pyc
   *.egg-info/
   .pytest_cache/
   venv/
   .venv/

   # Local copies of datasets and downloaded weights (never in git).
   /data/

   # Everything a run produces (checkpoints, MLflow's sqlite store, predictions, logs): per machine, never shared via git.
   experiments/
   ```
   `.gitattributes`: `*.sh text eol=lf` (CRLF breaks bash on the GPU host).
4. `src/<pkg>/core/registry.py`: a `Registry(kind)` class with `register(name)` (a decorator that refuses duplicates),
   `get(name)` (a `KeyError` that lists what is available), `build(name, **kwargs)` and `names()`. Copy it from
   `templates/registry.py` next to this file.
5. `scripts/tools/doc_toc.py`: copy it from `templates/doc_toc.py` and set its `DOCS` dict to the
   new repo's long docs.
6. Create the docs from §3 as stubs: a title, one paragraph saying which question the file answers, and a "Related
   documents" line. Fill the README's two tables (Document | Answers, Question | Home).
7. Write the first CHANGELOG entry in the long form: why this structure, and what was rejected.
8. Write `configs/templates/<stage>.yaml` with every knob at its default, plus a test that every config in
   `configs/<stage>/` has every key the template has.
9. First commit, in the §5 style. For example: `Initial skeleton: the registry, one template, the living docs`.
