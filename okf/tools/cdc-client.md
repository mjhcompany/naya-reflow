---
type: Tool
title: cdc-client.py
description: Reference Python CDC client — keymap and LED dump/set, aux telemetry, raw frames.
tags: [tool, python, cdc]
resource: ../../toolkit/cdc-client.py
generated:
  by: claude/claude-sonnet-5-5
  at: 2026-11-19T00:00:00Z
sources:
  - resource: ../../toolkit/README.md
---

Needs `pyserial`. Commands: `left|right dump`, `set KK spec`, `ledmap`, `dump100b`, `aux`, `raw TYPE C0C1 [params]`. Dumps land in `research/dumps/`. It is the Python twin of the web client's protocol core (same decoders and test vectors; see [web client](/software/web-client.md)). Protocol: [frame format](/protocol/cdc-frame-format.md).
