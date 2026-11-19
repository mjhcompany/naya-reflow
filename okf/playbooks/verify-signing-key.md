---
type: Playbook
title: Verify a claimed signing key
description: Prove a private key matches the stock KEYHASH before paying for it.
tags: [playbook, signing]
generated:
  by: claude/claude-sonnet-5-5
  at: 2026-11-19T00:00:00Z
sources:
  - resource: ../../docs/firmware-signing.md
---

```
pip install cryptography
python3 toolkit/verify-signing-key.py claimed-key.pem   # exit 0 = genuine
```

The script derives the public key, hashes it in common encodings, compares against the [KEYHASH](/firmware/signing-key.md) and does an RSA-PSS roundtrip. See [tool](/tools/verify-signing-key.md).
