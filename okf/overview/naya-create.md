---
type: Product
title: Naya Create keyboard
description: Split ergonomic keyboard by Naya B.V. (bankrupt 2026) with swappable Track/Touch/Tune modules.
tags: [product, keyboard]
generated:
  by: claude/claude-sonnet-5-5
  at: 2026-11-19T00:00:00Z
sources:
  - resource: ../../README.md
  - resource: ../../docs/hardware.md
---

# Summary

Split ergonomic keyboard, 74 keys per layer, 3 layers, two independent BLE halves plus optional USB dongle and docking modules. Vendor software was **NayaFlow** (Electron UI) driving **NayaCore** (native host daemon) over USB CDC. The company went bankrupt in 2026; this project preserves the knowledge needed to keep devices alive.

# Components

* [Halves](/hardware/halves.md) - left/right bases
* [Modules](/hardware/modules.md) - Track, Touch, Tune (+ two unreleased)
* [Dongle](/hardware/dongle.md) - nRF52840 BLE dongle

# Identifiers

* USB VID `0x37D1`; PID 100 = left, 200 = right
* Test units: left `387976F73EFE5420` ("Lilac Badger"), right `97BEE34FA0A74D9C` ("Focused Seal"), base FW 0.3.41.0
