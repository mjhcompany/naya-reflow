---
type: Playbook
title: Factory reset and restore customs
description: The 30/10ca clear-all-data ritual and how to bring layers and custom keys back.
tags: [playbook, reset, destructive]
status: stable
generated:
  by: claude/claude-sonnet-5-5
  at: 2026-11-19T00:00:00Z
sources:
  - resource: ../../docs/cdc-protocol.md
---

**Destructive.** Take a backup first (`toolkit/naya-backup.py`, see [backup/restore](/tools/backup-restore.md)).

1. Raw `30/10ca [01]` clears all data. A keymap/LED-only restore afterwards leaves **hold-to-layer dead** — the layer-list store is wiped and has no known write format.
2. Run a **stock NayaFlow flash**: it also enqueues `Profile(ADD_DEFAULT_DATA)`, restoring the layer engine. A write-verification error here is benign and reproducible.
3. Re-apply customs surgically with `30/1004` (params `[00, layer]+record`); the stock flash overwrote only 4 L0 records on the test unit. Verify readback IDENTICAL.

Related open bug: brightness steps wrap (50→…→10→100→…→0); wire probe showed the device clamps, so it is likely host-side arithmetic plus OFF-park interplay.
