# Claude Code setup

Written 2026-11-19, after running `/init` in this repo. Nothing described here is committed yet.

## What was set up

| File | Purpose |
|---|---|
| `CLAUDE.md` | Project instructions Claude Code loads in every session. |
| `.claude/skills/verify/SKILL.md` | `/verify`: runs the merge gate (build, oxlint, web smoke, Python smoke). |
| `.claude/skills/add-troubleshooting-recipe/SKILL.md` | Steps and invariants for a new Help-tab troubleshooting recipe. |
| `.claude/settings.json` | Hook: runs oxlint on each `.ts`/`.tsx` file under `client/web` after Claude edits it. |

### `CLAUDE.md` covers

- Commands, all from `client/web`: `npm run build` (the only typecheck), `npm run lint` (oxlint), and the two-step smoke run (`rolldown --config scripts/rolldown.smoke.mjs`, then `node /tmp/smoke.cjs`).
- Device safety: the never-send wire verbs (`fa/*`, `ee/10be`, `ee/10ae`, `30/10ca`) and the write rules (left half only, `isWriteAck`, `NayaSession.writeLed`, the layer byte on `30/1004`, the queue for length-changing writes).
- The four places a snapshot schema bump touches: `utils.ts`, `importers.ts`, `package.json`, and a new smoke section.
- TypeScript constraints: `import type`, no enums or namespaces, relative imports.
- Commit subject style: `Area sub: description`.

### Decisions recorded in `CLAUDE.md`

These came from questions answered during setup:

1. **This fork is live.** The README archive notice points to create-reflow, but `mjhcompany/naya-reflow` keeps being developed here.
2. **`fe/100a` needs a human decision.** The docs say never send it; `wire-guard.ts` allows it and a smoke check expects that. Claude asks before adding or changing code that sends it.
3. **Branch plus PR.** Work happens on a branch with a PR against `main`; no direct commits to `main`.

### The lint hook

- Fires after Write or Edit, only for `.ts`/`.tsx` files under `client/web`.
- Runs `client/web/node_modules/.bin/oxlint` on the edited file. Lint errors are fed back to Claude (exit code 2); warnings are not.
- Does nothing when `node_modules` is missing.
- It was created mid-session, so it only becomes active after opening `/hooks` once or restarting Claude Code.

## Verification done on 2026-11-19

- Hook command: tested by piping payloads into it. A clean file and a non-web file exit 0; a file breaking the hooks rule exits 2 with the oxlint error. Not yet seen firing on a real edit (see above).
- Merge gate, after `npm ci` in `client/web`:
  - `npm run build`: passes.
  - `npm run lint`: no errors. Existing warnings in `src/App.tsx` about reading refs during render (lines 541 and 617).
  - Web smoke: 402 ok, 0 FAIL.
  - `python3 scripts/smoke.py`: exit 0.

## Follow-ups from setup

- [ ] Add smoke and lint to CI. `deploy-pages.yml` only builds, so a failing smoke check can still deploy.
- [ ] Resolve the `fe/100a` contradiction, then replace the "ask first" note in `CLAUDE.md` with the real rule.
- [ ] Add a formatter (Prettier or Biome). Quote style varies by file today.
- [ ] Optional plugins: `/plugin install frontend-design@claude-plugins-official`, `/plugin install playwright@claude-plugins-official`, `/plugin install skill-creator@claude-plugins-official`.

See also `docs/project-state.md` and `docs/roadmap-proposal.md`.
