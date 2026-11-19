---
type: Software Component
title: Troubleshooting recipes plugin system
description: Help-tab plugin architecture in the web client; each recipe is one module under src/lib/troubleshooting/.
tags: [software, help, troubleshooting]
resource: ../../client/web/src/lib/troubleshooting/
generated:
  by: claude/claude-sonnet-5-5
  at: 2026-11-19T00:00:00Z
sources:
  - resource: ../../client/web/src/lib/troubleshooting/index.ts
---

Recipes are registered through `index.ts` with shared types in `types.ts`. Existing recipes: battery-odd, brightness-capped, brightness-wrap, dark-half, layers-dead, module-missing, override-silent, partial-flash, port-busy, right-cdc-deaf, steppy-anim, transport-sulk, undark, wire-guard. Each corresponds to a failure mode documented in [protocol](/protocol/) or [playbooks](/playbooks/), e.g. `undark` → [dark LED recovery](/playbooks/dark-led-recovery.md).
