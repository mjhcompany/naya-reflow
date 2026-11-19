#!/usr/bin/env python3
"""Validate okf/ against OKF v0.2 conformance (stdlib only).

Errors (exit 1): non-reserved .md without frontmatter or with empty `type`;
index.md frontmatter other than okf_version in the root; log.md date headings
not `## YYYY-MM-DD` or not newest-first.
Warnings (exit 0): broken links, missing description/title (spec tolerates them
but this repo's rules in CLAUDE.md require them).
Usage: scripts/okf-validate.py [bundle_dir]   (default: okf)
"""
import os, re, sys

root = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "okf")
errs, warns = [], []

for d, _, files in os.walk(root):
    for f in sorted(files):
        if not f.endswith(".md"):
            continue
        p = os.path.join(d, f)
        rel = os.path.relpath(p, root)
        t = open(p, encoding="utf-8").read()
        fm = re.match(r"---\n(.*?)\n---\n", t, re.S)
        if f == "index.md":
            if fm and rel != "index.md":
                errs.append(f"{rel}: index.md must have no frontmatter")
            elif fm and not re.fullmatch(r'okf_version:\s*"?[\d.]+"?', fm.group(1).strip()):
                errs.append(f"{rel}: root index.md frontmatter may only hold okf_version")
        elif f == "log.md":
            dates = re.findall(r"^## (.*)$", t, re.M)
            for x in dates:
                if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", x):
                    errs.append(f"{rel}: bad date heading '## {x}'")
            good = [x for x in dates if re.fullmatch(r"\d{4}-\d{2}-\d{2}", x)]
            if good != sorted(good, reverse=True):
                errs.append(f"{rel}: entries must be newest first")
        else:
            if not fm:
                errs.append(f"{rel}: missing YAML frontmatter")
                continue
            y = fm.group(1)
            if not re.search(r"^type:\s*\S", y, re.M):
                errs.append(f"{rel}: missing or empty `type`")
            for k in ("title", "description"):
                if not re.search(rf"^{k}:\s*\S", y, re.M):
                    warns.append(f"{rel}: no `{k}` (required by repo rules)")
        for l in re.findall(r"\]\(([^)\s#]+)", t):
            if re.match(r"[a-z]+:", l):
                continue
            tgt = os.path.join(root, l.lstrip("/")) if l.startswith("/") else os.path.join(d, l)
            if not os.path.exists(tgt):
                warns.append(f"{rel}: broken link {l}")

for w in warns: print("warn:", w, file=sys.stderr)
for e in errs: print("ERROR:", e, file=sys.stderr)
print(f"okf-validate: {len(errs)} error(s), {len(warns)} warning(s)")
sys.exit(1 if errs else 0)
