# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Status

The README carries an archive notice pointing to create-reflow. Ignore it: `mjhcompany/naya-reflow` is a fully separate project forked from the archived original, developed here, with no plan to follow or converge with create-reflow. The owner has a Naya Create for testing; "proven" results in the docs come from the original author's unit and are not yet re-verified on ours. Do take the notice's warning seriously that `docs/`, `research/` and `toolkit/` findings date from Sep–Oct 2026 and may be outdated; when a doc and the code disagree, say so rather than picking one silently.

## Layout

No root manifest. `client/web/` (React 19 + TypeScript + Vite + Tailwind v4, npm) is the only packaged project. `toolkit/` and `scripts/smoke.py` are standalone Python scripts (need `pyserial`). `toolkit/cdc-client.py` is the Python twin of the web protocol core: frame vectors must stay byte-identical between the two.

## Commands

Run from `client/web`:

- `npm run build` — `tsc -b && vite build`. This is the only typecheck.
- `npm run lint` — oxlint.
- Smoke tests (no `npm test` exists), two steps:
  ```
  ./node_modules/.bin/rolldown --config scripts/rolldown.smoke.mjs
  node /tmp/smoke.cjs   # pass = no FAIL lines
  ```
  `rolldown.smoke.mjs` is a rolldown config, not a runner; `node scripts/rolldown.smoke.mjs` does nothing. The cwd must be `client/web`. There is no way to run a single check.

From the repo root: `python3 scripts/smoke.py` (exit 0 = green).

Before every commit: build passes, both smokes pass, lint is clean for touched files. CI only builds and deploys to GitHub Pages; it runs neither lint nor smoke. `/verify` runs the whole gate.

## Device safety

Wire traffic goes to a real keyboard, and some verbs brick or wipe it.

- Never send, and never add code that sends: `fa/1002` and `fa/1006` (format/erase), `ee/10be` and `ee/10ae` (DFU/MCUboot resets), `30/10ca` (factory format; wipes the layer-list store, and only a stock NayaFlow flash restores it). These stay text-only recipes, never buttons.
- `fa/1001` is the one `fa` verb in normal use: the session's wake/identify probe (`lib/naya.ts`). Troubleshooting recipes may not use any `fa/*`; `assertWireAllowed` in `client/web/src/lib/troubleshooting/wire-guard.ts` refuses the whole group plus the verbs above. Do not loosen it.
- `fe/100a` is SET ACTIVITY TIMEOUTS (13 bytes), and the web client sends it for the timeout sliders. Older parts of the docs call it a "commit"; that is stale. Never replay captured `fe/100a` bytes as a commit: that wedged the device. Ask the user before adding any new code path that sends `fe/100a`.
- An ACK proves the device parsed a frame, not that it applied it. Confirm writes by reading back.
- Malformed short `ed/*` writes zero NVS settings, and oversized frames wedge the parser. Build frames with the existing helpers.
- Writes go to the LEFT half only.
- Validate write ACKs with `isWriteAck(ack, layer)`, never a strict `00 00` compare.
- LED writes go through `NayaSession.writeLed`; do not hand-roll them.
- `30/1004` params must be `[00, layer] + record`. Without the layer byte the device ACKs but applies nothing.
- Length-changing `30/1004` writes do apply. The older "silently ignored" rule in `toolkit/README.md` and elsewhere was refuted (see `docs/cdc-protocol.md`). Replacing a T10 key with a plain action must also clear its shadow slot at `KK+0x52`; `lib/queue.ts` and `lib/t10.ts` handle that, so queue key changes through them.
- Toolkit write scripts are dry-run by default and need `--apply`. Do not pass `--apply` without being asked.

## Snapshot schema

Bumping the export/backup format touches four places together: `SNAPSHOT_VERSION` in `client/web/src/lib/utils.ts`, a new link in `migrateSnapshot` in `src/lib/importers.ts` (`if ((obj.v ?? 1) < N) { …; obj.v = N; }`, oldest first), `naya.snapshotVersion` in `client/web/package.json`, and a new smoke section. Smoke fails if the constant and `package.json` drift.

## TypeScript

- `verbatimModuleSyntax`: use `import type` for types.
- `erasableSyntaxOnly`: no enums, namespaces or constructor parameter properties.
- No path aliases; imports are relative.
- No formatter is configured. Match the quote style of the file you are editing (it varies by file).
- UI: single accent color, no gradients, no shadows, tabular numbers, Lucide icons.

## Git

- Work on a branch and open a PR against `main`; do not commit directly to `main`.
- Commit subject: `Area sub: description`, lowercase after the colon, no trailing period, e.g. `Web keys: per-key notes w/ schema v2`, `Toolkit: …`, `Docs: …`. No conventional-commit prefixes.

## OKF knowledge bundle (`okf/`)

`okf/` is an Open Knowledge Format v0.2 bundle (spec: GoogleCloudPlatform/open-knowledge-format `SPEC.md`) holding the distilled hardware, protocol, firmware and tooling knowledge. `docs/` and `research/` remain the raw sources.

**Use it**
- Before any task touching the device, the CDC protocol, firmware or `toolkit/`, read `okf/index.md` and the relevant concepts (start with `okf/overview/project-status.md`). Follow their warnings and playbooks; they restate the Device safety rules above.
- If a concept contradicts the code, `docs/` or a live observation, say so rather than choosing silently, then fix the concept.

**Keep it correct** (changes to `okf/` or to anything it summarises)
- One concept per `.md` file; concept ID = path without `.md`. Reserved names: `index.md` (listing, no frontmatter; only the root one may carry `okf_version: "0.2"`) and `log.md`. Never use them for concepts.
- Every other file starts with YAML frontmatter with a non-empty `type`. In this repo also always set `title`, `description` (one sentence), `tags`, `generated: {by, at}` and `sources` (relative paths to the repo files the claim comes from). `at` is ISO 8601 with a UTC offset.
- Never add `verified` unless a human actually reviewed the concept (`by: human:<id>`).
- Link with bundle-relative paths (`/protocol/x.md`). Body is structured markdown (tables, lists, fenced code), no required headings.
- New concept → add it to its directory's `index.md` (`* [Title](file.md) - description`). Any change → add a `## YYYY-MM-DD` entry at the top of `okf/log.md` (newest first; start with **Creation**, **Update** or **Deprecation**).
- When you change `docs/cdc-protocol.md`, wire formats in `client/web/src/lib/` or `toolkit/` behavior, update the matching concept in the same change; bump its `generated.at` or set `status: deprecated`.
- Run `python3 scripts/okf-validate.py` (exit 0 required; a hook runs it after each edit under `okf/`). Run it before every commit that touches `okf/`.
