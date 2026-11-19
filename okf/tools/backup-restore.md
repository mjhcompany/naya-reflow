---
type: Tool
title: Backup, restore and stock-backup builder
description: naya-backup.py, naya-restore.py and build-stock-backup.py for snapshotting and replaying device state.
tags: [tool, backup, restore]
generated:
  by: claude/claude-sonnet-5-5
  at: 2026-11-19T00:00:00Z
sources:
  - resource: ../../toolkit/README.md
---

* `naya-backup.py` — read-only snapshot of the left half to JSON: keymap L0–L2, LED maps, reference telemetry.
* `naya-restore.py` — replays a snapshot via per-record `30/1004` + `30/100e` writes with readback (`IDENTICAL`/`DIFFERS`). Dry run by default; `--apply` writes. Length-changing rewrites may be ignored by the device.
* `build-stock-backup.py` — turns device dumps into a NayaFlow-acceptable `zip{backup_meta.json, user-data.db}`; `--verify` compares without writing. (Stock NayaFlow restore just reloads the app, so this is of limited value.)

Related: [factory reset ritual](/playbooks/factory-reset-ritual.md).
