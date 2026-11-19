---
type: Protocol
title: Module telemetry (de/ and fe/ reads)
description: How dock presence, module type, firmware version and battery voltage appear on the wire.
tags: [protocol, modules, battery]
generated:
  by: claude/claude-sonnet-5-5
  at: 2026-11-19T00:00:00Z
sources:
  - resource: ../../docs/modules.md
  - resource: ../../docs/cdc-protocol.md
---

* `de/1001` = `[00, PRESENT, TYPE|HALF, X]` — **byte 1 is the true presence flag**. TYPE: Touch=0x10, Track=0x20; bit 0 = half (0 left, 1 right).
* `de/1008` (left only) = `[00, TYPE, FLAG, 00, VER0, VER1, VER2]`; `02 03 03` = module FW 0.2.3.3. An earlier "battery byte" theory was CRC bytes misread.
* `de/100b` = `[00, HI, LO, 00]` module-rail voltage, big-endian mV (full Touch 4196, discharged Track 3714). Empty-dock: right reports zeros, left floats ~0x1060 — never use it for presence.
* `de/1009` = `[00][batt u16BE 0.1 mV][usb u16BE 0.1 mV]`; USB < 4.5 V implies Qi charging.
* `fe/1006` bytes 1–2 BE = base battery mV.

Hardware context: [modules](/hardware/modules.md), [power architecture](/hardware/power-architecture.md).
