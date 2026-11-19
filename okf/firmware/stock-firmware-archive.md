---
type: Firmware Artifact
title: Stock firmware archive
description: 15 MCUboot images carved from NayaFlow releases 0.1.1–1.25.1, covering all base epochs and the module image.
tags: [firmware, backup, mcuboot]
resource: ../../backup/firmware/
generated:
  by: claude/claude-sonnet-5-5
  at: 2026-11-19T00:00:00Z
sources:
  - resource: ../../backup/firmware/README.md
---

Images are carved from NayaCore binaries by `toolkit/extract_fw.py` (byte-identical across x64/arm64 builds). Each has an MCUboot header (placeholder `ih_ver` 1.2.3), **encrypted** body, TLV auth area and 0xFF padding trimmed. File names: `v<flow>_<name>_sz<img_size>_<hash8>.bin`.

| NayaFlow | Images (img_size) |
|---|---|
| 0.1.1 | 313392 base-left, 235296 base-right, 175136 module (identical through 1.6.10) |
| 1.3.11 (= 1.6.10) | 352256 L, 239184 R |
| 1.11.11 | 358496 L, 243840 R |
| 1.15.1 | 361632 L, 244336 R |
| 1.21.0 | 312272 L, 220688 R |
| 1.25.1 (base FW 0.3.41.0) | 328880 ×2, 226000 ×2 (the pairs differ; `_64` second HW revision) |

All share one [signing key](signing-key.md). NayaFlow installers are mirrored separately in `backup/software/` (manifest + fetch script; binaries are GitHub Release assets).
