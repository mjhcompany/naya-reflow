---
type: Project Status
title: Project status and reliability
description: What naya-reflow has solved, what is open, and why most research here is outdated.
tags: [status, caveat]
generated:
  by: claude/claude-sonnet-5-5
  at: 2026-11-19T00:00:00Z
stale_after: 2027-05-19T00:00:00Z
sources:
  - resource: ../../README.md
---

# Read this first

The repository is **archived**. Development moved to create-reflow (`@create-reflow/client`, `@create-reflow/sdk`). Research reflects knowledge as of **Sep–Oct 2026**; several results were later corrected. Treat everything in this bundle as historical unless confirmed in create-reflow.

# Status table

| Area | State |
|---|---|
| USB CDC protocol | Decoded: frames, CRC, keymap read/write, LED colors, module presence — see [frame format](/protocol/cdc-frame-format.md) |
| Independent key remapper | Works without NayaFlow — see [remap playbook](/playbooks/remap-key-without-nayaflow.md) |
| LED per-key colors | Formula closed: `[KK, Hue_lo, Hue_hi, Sat]` — see [LED map](/protocol/led-map-and-ed-interface.md) |
| Hardware identification | nRF52811 halves, STM32F411 modules, nRF52840 dongle |
| BLE custom pipe `0x1234` | Not an event channel — see [BLE pipe](/protocol/ble-pipe-1234.md) |
| Bootloader serial recovery | Closed; IMAGE group compiled out — see [MCUboot recovery](/protocol/bootloader-serial-recovery.md) |
| Signing-key buyout | One key signs all 15 images — see [signing key](/firmware/signing-key.md) |
| Module battery source | Open (voltage found; % is host-computed) |
| Color *write* command | Open at time of writing (per-key `30/100e` writes work) |
| Open firmware (ZMK) | Blocked on USB-MCU identity + pinout |

# Biggest open hardware question

Identity and pinout of the second (USB) MCU inside the halves — see [Halves](/hardware/halves.md).
