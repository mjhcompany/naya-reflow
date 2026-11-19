---
type: Hardware Component
title: Dock modules (Track, Touch, Tune)
description: Swappable input modules docked via wired pogo pins; STM32F411-based, flashed through the base.
tags: [hardware, modules, stm32]
generated:
  by: claude/claude-sonnet-5-5
  at: 2026-11-19T00:00:00Z
sources:
  - resource: ../../docs/modules.md
  - resource: ../../docs/hardware.md
---

# Types

NayaCore references **five** `*_UserApp.sfb` images; only three shipped.

| Module | Input | Shipped |
|---|---|---|
| Track | trackball + 4 buttons | yes |
| Tune | dial + 1–4 finger touch surface | yes |
| Touch | touchpad, 1–4 finger gestures | yes |
| Float | dial + 3D nav (rotation/translation x/y/z) | no |
| Query | no input gestures (probably output-only) | no |

# Hardware

* MCU STM32F411CEU6 (Cortex-M4F, 512 KB) on `Touch_MB 20250227 V10`; Qi receiver Maxic MT5705 (charging only)
* Link to base is **wired pogo pins**, no module radio
* Module FW 0.2.3.3 on test units; images live in the base's SPI flash (LittleFS) and are flashed via MCUboot through the base

# Presence and telemetry

Decoded in [module telemetry](/protocol/module-telemetry.md). Power path: [power architecture](power-architecture.md).

# Quirk

Module enablement is per-half in the keymap profile. After re-seating, a module can show DISABLED in NayaFlow until the profile is re-flashed; hardware is fine.
