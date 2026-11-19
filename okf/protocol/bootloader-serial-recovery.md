---
type: Protocol
title: MCUboot serial recovery (SMP over CDC)
description: How the bootloader's serial recovery mode behaves, what is compiled out, and how to unwedge it.
tags: [protocol, mcuboot, bootloader]
generated:
  by: claude/claude-sonnet-5-5
  at: 2026-11-19T00:00:00Z
sources:
  - resource: ../../docs/cdc-protocol.md
---

* Enter via app CDC `ee/10ce`: USB drops ~0.13 s, reappears ~0.9 s with an **extra** CDC node; recovery window ~2.2 s. ACM1 = command channel, ACM2 = boot log only.
* Banner: MCUboot on Zephyr 3.7.
* Framing: classic mcuboot-serial: `06 09` + base64(u16 len BE ‖ nmgr hdr ‖ CBOR ‖ crc16) + `\n`; CRC16 XMODEM poly 0x1021, **seed 0x0000**.
* DEFAULT group works (echo id 0, reset id 5). **IMAGE group is compiled out** — no serial upload or slot listing.
* Any valid frame resets the inactivity timer, so the device **parks** in recovery with the app protocol dead; flooding frames can also wedge the CDC driver.
* Consequence: firmware updates flow through the app CDC protocol into MCUboot's secondary slot; custom firmware is gated by [signing](/firmware/signing-key.md).

Recipe: [unwedge playbook](/playbooks/mcuboot-unwedge.md).
