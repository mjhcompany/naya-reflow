---
type: Protocol
title: LED map and ED debug interface
description: Per-key LED color records (30/100d, 30/100e) and the ED group that can persistently park the LED renderer.
tags: [protocol, led, danger]
generated:
  by: claude/claude-sonnet-5-5
  at: 2026-11-19T00:00:00Z
sources:
  - resource: ../../docs/cdc-protocol.md
---

# Per-key colors (safe)

* Read `30/100d`, write `30/100e` (per key, left port). Record: `[KK, Hue_lo, Hue_hi, Sat]`.
* Right-half color writes were never observed from NayaFlow; its LED map is not CDC-accessible.

# ED group (dangerous)

`ED/10xx` commands take `[target, value...]`, target uint8, `0xFF` = all. Brightness is **0–100** (nayactl's 0–255 is wrong).

| Cmd | Function |
|---|---|
| 1003/1004/1005 | ON / OFF / TOGGLE |
| 1008 | ADJ_BRT |
| 100E | HUE_SAT `[t, hue u16, sat 0-100]` |
| 1011 | SELECT EFFECT 0–3 = SOLID/BREATHE/SWIRL/SPECTRUM |
| 1012/1013/1014 | SCANMODE PWM / MAX BRIGHTNESS / LAYER OVERRIDE (no GET path) |
| 1050 | RGB_BRT global override — survives `ee/10ce` |

**Warning:** malformed (wrong-arity) ED writes persist garbage into NVS (`scanmode_pwm`, `led_layer_override`) and kept the left half dark through reboots and a NayaFlow full reset. NayaFlow itself never sends ED. Recovery: [dark LED recovery](/playbooks/dark-led-recovery.md).
