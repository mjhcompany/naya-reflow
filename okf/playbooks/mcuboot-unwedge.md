---
type: Playbook
title: Unwedge MCUboot serial recovery
description: Get a half back to the app after it parks in bootloader recovery or the console goes mute.
tags: [playbook, mcuboot, recovery]
generated:
  by: claude/claude-sonnet-5-5
  at: 2026-11-19T00:00:00Z
sources:
  - resource: ../../docs/cdc-protocol.md
---

Symptom: an extra CDC node persists, app protocol is dead, `cdc-client` wake hangs.

1. Release all port holders and idle 20–50 s so USB re-enumerates and the console revives.
2. Run `toolkit/smp-unwedge.py`: echo with CRC seed 0 on the command node (canary), then RESET (group 0, id 5, op 1).
3. Verify the app with `fa/1001`.

Proven 3×, no hands required. Background: [bootloader recovery](/protocol/bootloader-serial-recovery.md).
