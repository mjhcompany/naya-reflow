---
type: Finding
title: Single firmware signing key
description: All 15 stock images share one MCUboot KEYHASH, so one private key unlocks custom firmware for every component.
tags: [firmware, signing, mcuboot, fundraiser]
generated:
  by: claude/claude-sonnet-5-5
  at: 2026-11-19T00:00:00Z
sources:
  - resource: ../../docs/firmware-signing.md
---

# Fact

Every image in `backup/firmware/` (base epochs L/R incl. `_64` boards, plus module image) carries the same KEYHASH TLV (type 0x01):

```
de8b07187913e6e788306618e4166e38a8c2eda99b68970d17fd00e75fd5b972
```

TLV layout: `0x10` SHA256 (32 B) + `0x01` KEYHASH (32 B) + `0x20` RSA2048-PSS signature (256 B) + `0x30` ENCRSA2048 wrapped key (256 B).

# What to acquire

1. The RSA-2048 MCUboot signing **private** key matching the hash — alone sufficient to ship custom base + module firmware through the stock update path.
2. Nice-to-have: image-encryption keypair (probably unnecessary — MCUboot boots signed plain images; if rejected, recover the key via SWD).
3. Nice-to-have: NayaCore build scripts.

# Safety

MCUboot trial swap reverts a failing image automatically, so first builds cannot brick a daily-driver board; SWD pads remain the last resort. No donor board needed.

Verify a claimed key with [verify-signing-key](/tools/verify-signing-key.md) before any payment.
