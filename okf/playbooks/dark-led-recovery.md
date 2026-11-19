---
type: Playbook
title: Recover dark LEDs after bad ED writes
description: Restore the LED renderer when malformed ED commands parked it.
tags: [playbook, led, recovery]
generated:
  by: claude/claude-sonnet-5-5
  at: 2026-11-19T00:00:00Z
sources:
  - resource: ../../docs/cdc-protocol.md
---

Symptom: keys dark (module LED ok, typing fine) and not fixed by reboot or NayaFlow full reset. Cause: NVS-persisted LED settings — see [ED interface](/protocol/led-map-and-ed-interface.md).

# Left half

Send clean `[0xFF, value]` writes: 1013 max brightness=100, 1012 scanmode=1, 1014 override=0, 1050 white/100, 1008 brightness=100, 1011 SOLID, 1003 ON (plus RESUME). Scripted as `toolkit/naya-undark.py` (1013 ceiling + [FF]-phase bundle) and `naya-led-recover.py --phase ff`; both dry-run by default, `--apply` writes.

# Right half

ED ACKs but the render stays dark; its LED map is not CDC-accessible. Recovery that worked: hardware Layer 2 LED combos on the half itself (hold-2 corner key + brightness/effect keys), then force-reflash both halves and re-pair in NayaFlow.

# Notes

* A real reboot is `ee/10ce` or USB replug; the power switch with USB plugged is not an MCU reset.
* If it relapses, see the [factory reset ritual](factory-reset-ritual.md).
