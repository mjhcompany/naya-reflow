---
type: Software Component
title: Web client (client/web)
description: React/TypeScript WebSerial configurator that replaces NayaFlow; now continued as @create-reflow/client.
tags: [software, webserial, react]
resource: ../../client/web/
generated:
  by: claude/claude-sonnet-5-5
  at: 2026-11-19T00:00:00Z
sources:
  - resource: ../../client/web/README.md
---

# Requirements

Chromium browser (WebSerial), https or localhost, NayaFlow closed, udev rule on Linux.

# Develop

```
cd client/web
npm install
npm run dev     # http://localhost:5173/
npm run build   # tsc -b + vite -> dist/
```

Protocol regression tests need no hardware: build `scripts/rolldown.smoke.mjs` with rolldown, run the output, expect no FAIL lines. Deployed to GitHub Pages from `main`.

# Features

Dual-half auto-connect (VID `0x37D1`), 3-layer read, keyboard/layout views, multi-select editor with action palette and colors, local draft with flash preview and readback verify, battery/module pills, JSON export, per-key notes, activity-timeout settings, categorized CDC log.

# Layout

* `src/lib/naya.ts`, `aux.ts`, `t10.ts`, `draft.ts`, `queue.ts` — protocol core and write queue
* `src/lib/actions.ts`, `palette-groups.ts`, `kb-data.ts`, `key-icons.ts` — action vocabulary, keycap geometry, icons
* `src/hooks/` — sessions, layers, draft, flash, selection, aux polling
* `src/components/` — UI; `src/lib/troubleshooting/` — [recipes](web-troubleshooting-recipes.md)

Python twin: [cdc-client](/tools/cdc-client.md).
