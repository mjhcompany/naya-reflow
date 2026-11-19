---
name: verify
description: Run this repo's full merge gate (web build/typecheck, oxlint, web smoke bundle and run, Python smoke) and report the result. Use before committing or opening a PR, or when asked to verify, test or check changes.
---

Run the merge gate and report what passed and what failed. CI does not run lint or smoke, so this is the only check.

Run steps 1–4 from `client/web`, step 5 from the repo root. Keep going after a failure so the report covers every step.

1. If `client/web/node_modules` is missing, run `npm ci` first.
2. `npm run build` — typecheck plus Vite build. Must exit 0.
3. `npm run lint` — oxlint. Errors fail the gate; report warnings only for files changed on this branch.
4. Web smoke, in two steps, with cwd `client/web`:
   ```
   ./node_modules/.bin/rolldown --config scripts/rolldown.smoke.mjs
   node /tmp/smoke.cjs
   ```
   The first command bundles to `/tmp/smoke.cjs` (hardcoded); the second runs it. Passing means exit 0 and no line starting with `FAIL`. Do not run `node scripts/rolldown.smoke.mjs`; it is a config and does nothing.
5. `python3 scripts/smoke.py` from the repo root. Must exit 0.

Report one line per step with pass or fail. For failures, quote the exact `FAIL` lines or compiler errors. Do not call the gate green unless every step ran and passed; if a step could not run, say which and why.

If a smoke check fails because behavior changed on purpose, do not edit the expected value on your own. Show the user the check and ask.
