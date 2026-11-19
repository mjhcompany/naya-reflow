---
type: Tool
title: Capture and probing tools
description: Sniffer, syscall interposer, firmware extractor, BLE scanner and SMP probes used for reverse engineering.
tags: [tool, reverse-engineering]
generated:
  by: claude/claude-sonnet-5-5
  at: 2026-11-19T00:00:00Z
sources:
  - resource: ../../toolkit/README.md
---

* `cdc-sniff.py` — passive serial logger (timestamps, hex)
* `interposer.c` — macOS `DYLD_INSERT_LIBRARIES` tap on NayaCore's serial read/write; stock binaries strip `DYLD_*`, so use a re-signed clone
* `extract_fw.py` — carves images into the [firmware archive](/firmware/stock-firmware-archive.md)
* `ble-scan.py` — bleak-based advertisement scan
* `smp-probe4..8.py`, `smp-unwedge.py`, `boot-trap.py` — bootloader work ([protocol](/protocol/bootloader-serial-recovery.md))
* `naya-*-spike.py` — dry-run-by-default experiments: T10 write (proven), module-slot `30/100c` write (proven), `ed/1011` effect (proven), `30/100e` batch write (dead)
* `naya-maxbrt.py`, `naya-undark.py`, `naya-led-recover.py` — LED fixes ([playbook](/playbooks/dark-led-recovery.md))

Raw outputs live in `research/` (captures, dumps, FCC reports, disassembly extracts).
