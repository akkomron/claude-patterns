"""Write (or refresh) a linked table of contents at the top of long markdown docs.

    python scripts/tools/doc_toc.py                      # every doc in DOCS below
    python scripts/tools/doc_toc.py docs/DATA.md --depth 3

The contents list goes between `<!-- toc:start -->` and `<!-- toc:end -->`; if a file has no markers, they are inserted right
after its title (the first `# ` line). Headings inside fenced code blocks are skipped. Anchors follow GitHub's rule (lower
case, punctuation dropped, spaces to hyphens, duplicates suffixed -1, -2), so the links work on GitHub and in VS Code's preview.
Rerun after adding or renaming a section; the block is regenerated, never edited by hand.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

START, END = "<!-- toc:start -->", "<!-- toc:end -->"
# the long docs and how deep their contents go (## = 2, ### = 3); edit per repo
DOCS = {"docs/DATA.md": 3, "docs/STRATEGY.md": 3, "docs/HYPOTHESES.md": 3, "docs/EXPERIMENTS.md": 2}


def slug(text: str) -> str:
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)      # [label](link) -> label
    text = text.replace("`", "").lower()
    return "".join(ch for ch in text if ch.isalnum() or ch in " -_").replace(" ", "-")


def headings(lines: list[str], depth: int) -> list[tuple[int, str, str]]:
    out, seen, fence = [], {}, False
    for line in lines:
        if line.lstrip().startswith(("```", "~~~")):
            fence = not fence
            continue
        m = re.match(r"^(#{2,6})\s+(.*?)\s*#*\s*$", line)
        if fence or not m or len(m.group(1)) > depth:
            continue
        title = m.group(2)
        base = slug(title)
        n = seen.get(base, 0)
        seen[base] = n + 1
        out.append((len(m.group(1)), title, base if n == 0 else f"{base}-{n}"))
    return out


def toc_block(items: list[tuple[int, str, str]]) -> list[str]:
    body = []
    for level, title, anchor in items:
        shown = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", title)
        body.append(f"{'  ' * (level - 2)}- [{shown}](#{anchor})")
    return [START, "**Contents**", "", *body, END]


def update(path: Path, depth: int) -> None:
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    if START in lines and END in lines:
        i, j = lines.index(START), lines.index(END)
        rest = lines[:i] + lines[j + 1:]
        items = headings(rest, depth)
        lines = lines[:i] + toc_block(items) + lines[j + 1:]
    else:
        items = headings(lines, depth)
        title = next(k for k, l in enumerate(lines) if l.startswith("# "))
        lines = lines[:title + 1] + [""] + toc_block(items) + lines[title + 1:]
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"{path}: {len(items)} entries")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("files", nargs="*", type=Path)
    parser.add_argument("--depth", type=int, default=None, help="deepest heading level listed (default: per DOCS, else 3)")
    args = parser.parse_args()
    targets = [(f, args.depth or DOCS.get(f.as_posix(), 3)) for f in args.files] or \
              [(Path(f), args.depth or d) for f, d in DOCS.items()]
    for f, d in targets:
        update(f, d)


if __name__ == "__main__":
    main()
