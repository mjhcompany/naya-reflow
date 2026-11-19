---
type: Protocol
title: USB CDC frame format
description: Binary framing, addressing and XOR checksum used between NayaCore and each keyboard half.
tags: [protocol, cdc, usb]
resource: ../../docs/cdc-protocol.md
generated:
  by: claude/claude-sonnet-5-5
  at: 2026-11-19T00:00:00Z
sources:
  - resource: ../../docs/cdc-protocol.md
---

# Transport

USB CDC-ACM, one data port per half (VID `0x37D1`, PID 100 left / 200 right). Baud rate is ignored. Set DTR/RTS like Qt does. The half must be **awake and in USB mode**; a sleeping half answers nothing. NayaFlow holds the ports exclusively — quit it first.

# Frames

```
Request:  AA | 00  | DST | 00 | TYPE | LEN | C0 C1 | PARAMS... | CRC | 04
Response: AA | SRC | 00  | 00 | TYPE | LEN | C0 C1 | PAYLOAD... | CRC | 04
```

* DST/SRC: `0x50` left half, `0x51` right half
* LEN = len(C0 C1 + params/payload)
* **CRC = XOR** of `frame[6:-2]` (C0 through end of payload); verified on 269 captured frames
* Response header byte 3 = remaining-parts counter for multi-part reads; payload byte 0 = more-flag, byte 1 = layer echo
* Responses arrive in request order per port

# Status vocabulary

`Invalid command / Invalid format / Invalid ID / Memory full / Save failed / Load failed / No data / NVS`

# Gotchas

* **Never replay captured `fe/100a` bytes** as a "commit": `30/1004` writes persist on their own, and `fe/100a` is actually SET ACTIVITY TIMEOUTS (13 B: status 00 + 3×u32LE ms). Stale replays wedged the device (reboot recovers).
* NayaCore↔NayaFlow also uses CBOR messages and ZMQ — separate from this wire protocol.

Commands: [command groups](cdc-command-groups.md). Python implementation: [cdc-client](/tools/cdc-client.md).
