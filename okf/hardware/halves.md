---
type: Hardware Component
title: Halves (NAYA-800-1)
description: Left and right keyboard bases — nRF52811 BLE SoC plus an unidentified USB MCU.
tags: [hardware, halves, nrf52811]
generated:
  by: claude/claude-sonnet-5-5
  at: 2026-11-19T00:00:00Z
sources:
  - resource: ../../docs/hardware.md
---

| Item | Value |
|---|---|
| BLE SoC | Nordic nRF52811 (inferred: FCC tests pass 125 kbps coded PHY, which nRF52810 lacks) |
| USB MCU | **Unknown** — nRF has no USB; halves expose CDC + HID; FW images 226–360 KB exceed nRF flash |
| Boards | `Create_L_KB_20250220_V13` / `Create_R_KB_20250221_V13` |
| Switches | Kailh CPG-1232 low-profile |
| Base cells | 3.7 V 50 mAh — hot-swap buffers, not runtime source |
| USB | VID `0x37D1`, PID 100 (left) / 200 (right); CDC-Control + CDC-Data + HID |
| Toolchain | nRF Connect SDK; bootloader is MCUboot on Zephyr 3.7 |
| Debug | SWDIO/SWDCLK test points at the USB-C corner |

Each half is an independent BLE peripheral (HID over GATT + custom [`0x1234` service](/protocol/ble-pipe-1234.md)); the host merges them. No radio link between halves.

# Hardware revisions

HwID selects firmware image `kb_fw*` vs `kb_fw*_64` (second board revision, only in NayaFlow ≥ 1.25.1). See [firmware archive](/firmware/stock-firmware-archive.md).

# Open question

USB MCU identity + pinout is the blocker for a ZMK port. Everything else needed is known.
