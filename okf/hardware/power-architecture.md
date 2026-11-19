---
type: Finding
title: Bidirectional pogo power architecture
description: Off-USB the halves run from the docked modules; the 50 mAh base cells only bridge hot-swaps.
tags: [hardware, power, battery]
generated:
  by: claude/claude-sonnet-5-5
  at: 2026-11-19T00:00:00Z
sources:
  - resource: ../../docs/modules.md
---

* USB → base → module when plugged; module → base when unplugged (VBUS both ways over pogo)
* Base cells (50 mAh) are hot-swap buffers. To sag them in a discharge test, **undock** modules.
* Module packs ~600–1000 mAh (Track 1S2P 600 mAh, Touch ~1000 mAh class)
* Battery % is **host-computed**: base `KB% = (mV−3300)/9` clamped 0..100; module % from rail voltage (calibration: 4222 mV→100 %, 3910 mV→67 %, 3709 mV→45 %)
* Voltage sources on the wire: [`fe/1006` base mV, `de/100b` module rail mV](/protocol/module-telemetry.md)
