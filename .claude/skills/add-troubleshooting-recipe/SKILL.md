---
name: add-troubleshooting-recipe
description: Add or change an entry in the web client's troubleshooting knowledge base (client/web/src/lib/troubleshooting). Use when asked to add a troubleshooting recipe, problem, fix or runnable action to the Help tab.
---

Troubleshooting entries are plugins: one file per problem in `client/web/src/lib/troubleshooting/`. Read `types.ts` and one existing entry (for example `brightness-capped.ts`) before writing.

## Steps

1. Create `client/web/src/lib/troubleshooting/<kebab-id>.ts` that does `export default { … } satisfies TroubleEntry`. Use double quotes; this directory does.
2. Fill `id` (unique, matches the file name), `title`, `summary`, `details` and `steps` (the human recipe, numbered in the UI). All must be non-empty.
3. Import the entry in `index.ts` and add it to the `TROUBLES` array. An entry that is not in the array does not exist.
4. Run `/verify`. Smoke section 30 checks the invariants below.

## Actions

An action is optional. If the entry has one:

- Give it either declarative `steps: WireStep[]` or a scripted `run(ctx)`, never both.
- Set `side` to the half that must be connected: `left`, `right`, or `any` for app-side flows.
- Add `confirm` text to anything that mutates device state. Smoke requires it for every `side: "right"` action.
- In `run`, send only through `ctx.send`, which is guarded. Do not reach for the session directly.
- Every wire step must pass `assertWireAllowed`. Never add an action for `fa/*`, `ee/10be`, `ee/10ae` or `30/10ca`, and never weaken `wire-guard.ts` to make one pass. Those fixes stay text-only, with a warning in `details`.
- `fe/100a`: ask the user before adding an action that sends it.

## Sourcing

Recipes run against a real keyboard. Only add wire steps that are documented as proven (in `docs/cdc-protocol.md`, a toolkit script, or by the user). Say in a comment where the bytes come from. If the source is uncertain or the docs may be outdated, make the entry text-only and tell the user what would need confirming on hardware.
