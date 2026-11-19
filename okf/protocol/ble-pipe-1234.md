---
type: Finding
title: BLE GATT map and custom pipe 0x1234/0x5678
description: Verdict that the custom BLE characteristic is idle and not an input-event channel.
tags: [protocol, ble, gatt]
generated:
  by: claude/claude-sonnet-5-5
  at: 2026-11-19T00:00:00Z
sources:
  - resource: ../../docs/ble-pipe-1234.md
---

# GATT map (left half, bonded)

* 0x1800 Generic Access, 0x1801 Attribute, 0x180F Battery (0x2A19 notify), 0x180A Device Info, 0x1812 HID over GATT
* **0x1234** custom service with one characteristic **0x5678** [Notify, Read, Write]

# Verdict (2026-09-15)

Reading 0x5678 always returns static `0x65` (bonded or not); subscribing succeeds but zero notifications arrive during trackball/module activity while battery notifications keep flowing. Input reaches the host **only via standard HID reports** (Report ID 3 = mouse; report map saved in `research/ble/hid-report-map-left.bin`, 212 B). The pipe is probably a host→keyboard command channel; write probes were deferred because of wedge risk.

No proprietary radio exists — see [halves](/hardware/halves.md).
