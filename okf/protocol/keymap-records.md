---
type: Protocol
title: Keymap records and write path
description: Per-key binding record encoding (`[KK, T, LEN, payload]`) and how to read/write keys over CDC.
tags: [protocol, keymap, remap]
generated:
  by: claude/claude-sonnet-5-5
  at: 2026-11-19T00:00:00Z
sources:
  - resource: ../../docs/cdc-protocol.md
---

# Layout

3 layers × 74 keys. L0 starts Esc(0x29) Grave(0x35) 1(0x1E) 2(0x1F)… KK is the key index.

# Record types

Universal record: `[KK, T, LEN, payload]`. The wire T byte is the ZMK behaviour id.

| T | Len | Meaning |
|---|---|---|
| 01 | 7 | HID key: `[KK,01,04,HID,PAGE_BE,MOD]`; param = (mod<<24)\|(page<<16)\|hid; consumer keys use page `0x000c` |
| 05 | 7 | MO (momentary layer) |
| 08 | 7 | output select USB/BT |
| 00 / 09 / 0f | 11 | BT / LED / mouse (`[KK,T,08,X(4B),Y(4B)]`) |
| 07 / 0e | 3 | fillers |
| 06 | — | naya-type actions `[06,04,p1]` |
| 10 | 27 | multi-behavior pair (hold-tap); tapping term `c8 00` = 200 ms |
| 02,03,04,0a | — | unmapped |
| 0b,0c,0d | — | dead binding types (never on wire) |

# Writing

* Per-key write: `30/1004` with params **`[00, LAYER] + record`** — omitting the layer byte makes the device read KK as the layer, ACK with status 0x19 and apply nothing (survives reboot).
* Applied instantly and persists; no commit needed. Length-changing record rewrites can be silently ignored by the device.
* Readback via `30/1003`; always verify.
* Keymap-only 1004 writes do not break the layer store.

See [remap playbook](/playbooks/remap-key-without-nayaflow.md) and [backup/restore](/tools/backup-restore.md).
