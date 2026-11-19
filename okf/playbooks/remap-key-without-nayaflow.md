---
type: Playbook
title: Remap a key without NayaFlow
description: Read the keymap and rewrite a key over USB CDC using cdc-client.py.
tags: [playbook, remap]
generated:
  by: claude/claude-sonnet-5-5
  at: 2026-11-19T00:00:00Z
sources:
  - resource: ../../README.md
  - resource: ../../toolkit/README.md
---

1. Quit NayaFlow (it holds the serial ports); wake the half and use USB output mode.
2. `pip install pyserial`
3. `python3 toolkit/cdc-client.py left dump` — read all 3 layers
4. `python3 toolkit/cdc-client.py left set 30 hid:14` — KK30 → Q; applied instantly and persisted. Spec prefixes: `hid:`, `cons:`, `vend:`, `raw:`.
5. `python3 toolkit/cdc-client.py left ledmap` — read LED colors

Never replay captured `fe/100a` bytes. Take a [backup](/tools/backup-restore.md) first. Record format: [keymap records](/protocol/keymap-records.md). Browser alternative: [web client](/software/web-client.md).
