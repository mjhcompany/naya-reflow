# Roadmap proposal

Date: 2026-11-19. Status: proposal; the five framing decisions below are settled, the phases are not yet agreed. Based on `docs/project-state.md`; section numbers below refer to it.

## Decisions (made by the owner, 2026-11-19)

1. **Device:** a Naya Create is available for testing. Phase 3 is open, and phase 1 fixes get confirmed on hardware.
2. **Relationship to create-reflow:** none. This is a fully separate project forked from the old one. create-reflow is not a source of truth and there is no plan to converge. Findings here are established by our own tests on our own device.
3. **License:** agreed to ask the upstream author for one. Still to do.
4. **`okf/`:** stays, and is the knowledge base of this project. `docs/` and `research/` are the raw sources behind it. It therefore has to be correct: see phase 0.
5. **Vendor material and FCC files:** stay in git for now. Revisit later.

## Phase 0 — Make the fork yours and safe to change

No device needed. Small, mostly mechanical.

- [ ] Commit the Claude Code setup and these docs on a branch, via PR.
- [ ] Ask the upstream author to add a license; record the answer.
- [ ] OKF review pass. The bundle is marked "not human-reviewed" and repeats stale statements, at least: the length-changing-write rule (`okf/protocol/keymap-records.md`) and "colour write: open" / "module battery: open" (`okf/overview/project-status.md`). Check every concept against the latest entries in `docs/cdc-protocol.md` and the code, fix it, and log each change in `okf/log.md`.
- [ ] Record the device in `okf/`: serial-free description, firmware versions of both halves and modules, and its current state. The old handoff describes the upstream author's unit, not ours.
- [ ] Take a full backup of the device (`toolkit/naya-backup.py`, plus a stock NayaFlow backup if the app is still installed) before any write.
- [ ] CI: add a pull-request trigger and run lint, web smoke and Python smoke before deploy. Add `npm run smoke` and `npm run typecheck` scripts; write the smoke bundle to a path inside the project; add `rolldown` as a direct devDependency.
- [ ] Update `vite` to 8.3.8 or later and run `npm audit fix`.
- [ ] Fork identity: header link, `client/web/README.md` URL, release-asset scripts. Confirm Pages deploys from the fork.
- [ ] Replace the README archive notice with this project's own status: a separate project, forked from the archived original, with credit to it.
- [ ] Docs truth pass: fix the stale statements in section 5.4 (`fe/100a`, length-changing writes, README status table, `modules.md`, `competitor-gap.md`) in the READMEs. Leave `docs/cdc-protocol.md` as the historical lab log; `okf/` carries the current facts.
- [ ] Remove the dangling `AGENTS.md` reference in `wire-guard.ts`; record what "UHK #N" means or drop the tags.
- [ ] Add a formatter (Biome or Prettier) and a format-on-edit hook.

- [ ] CI: run `python3 scripts/okf-validate.py` too.

Exit: a PR cannot merge or deploy with failing smoke, `okf/` has been reviewed against the code, and the device is backed up.

## Phase 1 — Fix what is broken

No new protocol knowledge needed. Section 5.1 numbers in brackets.

- [ ] Wire the Tapping Term slider into the record builders and persist it [1].
- [ ] Apply notes on import and restore [2].
- [ ] Persist the draft queue across reloads [3].
- [ ] Surface serial reader errors at once; add cancel to Flash and a shorter worst-case timeout [4, 5].
- [ ] Show write-only settings as "unknown" until the user sets them, and do not queue on first touch [6].
- [ ] Read back after settings and module writes where a read exists; say so plainly where none does [7].
- [ ] Make multi-record key writes recoverable after a mid-set failure [8].
- [ ] Set the busy flag around module and timeout reads [9].
- [ ] Add a firmware-version check with a clear message for untested versions [10].
- [ ] Clear the 15 lint warnings; delete dead code and the duplicated helpers.
- [ ] Toolkit: fix `monitor.py`, add dry-run to `cdc-client.py` writes, add `requirements.txt` or `pyproject.toml`, support Linux port names.
- [ ] Tests: add a mocked-port harness that exercises the flash executor and the session's multipart path, which have no coverage today.

Exit: every control in the UI either does what it says or states that it cannot, and each device-facing fix is confirmed on the keyboard.

## Phase 2 — Fill gaps that need no reverse engineering

- [ ] Palette: keypad keys, the full consumer set, "Disabled" and "Transparent", layer actions for every layer.
- [ ] One-click full backup export and matching import, including timeouts and module config.
- [ ] Import of the stock NayaFlow backup zip in the browser.
- [ ] Layer names (stored locally and in exports).
- [ ] Keyboard-only editing and the accessibility items in section 5.2.
- [ ] Light theme.
- [ ] Split `naya.ts` into transport, session and decoders; reduce `BindingsTab` props.
- [ ] Rewrite `client/web/README.md` with current features and known limitations.

## Phase 3 — Research on the device

Ordered by user value. Before the first experiment, re-verify the basics on our unit (read, one key write, one LED write, backup and restore), because every "proven" result in the repo comes from a different unit on firmware 0.3.41.0.

1. **Layer-list write (`30/1002`).** Removes the dependency on the vendor app after a factory format. Highest value: the vendor app will eventually stop being obtainable.
2. **Right-half path.** How the right half gets its keymap and colours, and a right-side recovery for the dark state.
3. **Modifier mask on the wire.** Unlocks shifted keys and key combinations.
4. **Interrupt flavor encoding.** Turns the UI-only setting into a real one.
5. **Module settings** (pointer speed, acceleration, scroll) and palette-based gesture editing.
6. **Macros.** Find out first whether the firmware executes them at all.
7. **Stock firmware re-flash without NayaFlow.** Needs the upload protocol, which is undocumented.

Rule for this phase: every experiment gets a backup first, a written expected result, and a recorded verdict. The raw log goes in `docs/` or `research/`; the resulting fact goes into the matching `okf/` concept in the same change.

## Phase 4 — Long-horizon options

Not recommended to start now; listed so they are not forgotten.

- **Custom firmware.** Blocked on the signing key or an untried SWD route, plus an unidentified USB MCU. Worth revisiting only if the key becomes available or someone with hardware skills opens a board.
- **BLE and dongle configuration.** Nothing is known beyond a GATT listing.
- **Vendor material and FCC files in git** (decision 5): revisit once the project is public-facing.

## Suggested order

Phase 0 first and complete. Then phase 1, with bugs 1–3 at the front because users hit them directly. Phases 2 and 3 can then run in parallel: phase 2 is software-only, phase 3 needs time at the keyboard.
