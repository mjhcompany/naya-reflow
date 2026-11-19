---
type: Reference
title: CDC command groups
description: TYPE byte groups and the C0C1 command codes decoded from NayaCore.
tags: [protocol, cdc, reference]
generated:
  by: claude/claude-sonnet-5-5
  at: 2026-11-19T00:00:00Z
sources:
  - resource: ../../docs/cdc-protocol.md
---

Written `TYPE/C0C1`. Codes come from static RE of NayaCore plus empirical cross-checks.

| TYPE | Domain | Notable commands |
|---|---|---|
| `be` | BLE | 1002 GET PAIR ADDRESS, 1006/1007 GET/SET BLE NAME, 1008 GET BLE ADDRESS, 100C GET BLE STATUS (250 B), 100F GET BLE FW VERSION (`00 02 1d` = v0.2.29), 1010 CLEAR ALL SPLIT LINKS |
| `de` | Module | 1001 handshake / dock presence, 1002 detect, 1005 MODULE FWUP, 1008 GET MODULE FW VERSION, 1009 GET BATTERY, 100B GET PRECISE BATTERY LEVEL |
| `ee` | Reset | 10ce NORMAL RESET, 10be DFU RESET, 10ae MCU BOOT RESET |
| `fa` | Flash | 1001 TEST FLASH, 1002 FORMAT PARTITION, 1006 ERASE CHIP (destructive) |
| `fe` | System | 1002 GET FW VERSION (`00 03 29 00 38` = 0.3.41.0), 1004 GET HW ID, 1006 GET KB BATTERY (base mV), 1008 TOGGLE KEYSCAN, 1009 KEYSCAN EVENT, 100A/100B SET/GET ACTIVITY TIMEOUTS |
| `ff` | Misc | 1001 VERIFY FLASH, 1002 ENQUEUE READ LAYERS, 1003 GET MODULE INFO |
| `ed` | LED debug | see [ED interface](led-map-and-ed-interface.md) — **dangerous** |
| `30` | Remap | 1003 READ LAYER DATA, 1004 WRITE LAYER DATA, 1009–100C module config, 100D READ LED MAP, 100E WRITE LED MAP, 10ca CLEAR ALL DATA (nayactl) |
| `ca`, `f1` | — | no known commands |

Macro list/data commands (30/1005–1008) answer but the device store is empty — macros are host-only.

Related: [frame format](cdc-frame-format.md), [keymap records](keymap-records.md), [module telemetry](module-telemetry.md).
