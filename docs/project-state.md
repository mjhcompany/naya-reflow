# Project state

Audit date: 2026-11-19. Scope: the whole repository at commit `be23f89`, plus the uncommitted files added that day.

How to read this: **verified** means checked in code or by running a command during the audit. **Documented** means the repo's docs record it (often as a live device test by the upstream author); nothing here was re-tested on hardware. No device was available during the audit.

## 1. Summary

naya-reflow is an open-source revival of the Naya Create split keyboard after its vendor, Naya B.V., went bankrupt. It holds a reverse-engineered USB CDC protocol, a WebSerial configurator that replaces the vendor's NayaFlow app, Python tooling, firmware backups and raw research.

- **The web client works and is fairly complete** for everyday use: key remapping, tap/hold behaviors, per-key LED colours, animations, timeouts, backups and a troubleshooting tab. Build, lint and 402 smoke checks pass.
- **Protocol knowledge is solid for the left half's keymap and LEDs**, and thin or open for the right half, modules, macros, BLE and firmware.
- **All work happened in 12 days** (2026-09-15 to 09-26, 140 commits, one author). The upstream author then archived the repo and moved to `create-reflow`.
- **Custom firmware is not possible today.** Images are signed with a key nobody has, and no alternative entry has been tried.
- **A factory-formatted board cannot be fully recovered without the vendor app.** This is the largest functional gap.
- **The fork has housekeeping debt:** no license, upstream URLs, stale docs that contradict the code, CI that does not test, and 230 MB of FCC files in git.

## 2. Timeline

| Date (2026) | Commits | What happened |
|---|---|---|
| 09-15 | 15 | Firmware images extracted. CDC framing and CRC solved, first key write, LED map decoded, FCC filings added. |
| 09-16 | 22 | Module battery solved, colour write closed, MCUboot serial recovery explored, web client created, Pages deploy. |
| 09-17 | 42 | Static reverse-engineering peak: full command map, record types, first "dark half" incident and recovery. Parity plan and spec written. |
| 09-18 | 26 | Live spikes (multi-behavior keys, module write, effects). Web client phases 1–6. |
| 09-19 | 11 | Full-map LED batch write found dead. Length-change rule refuted. First factory-format incident. |
| 09-22 | 19 | Dark-half relapse, device handoff document, web UX series. |
| 09-26 | 4 | Troubleshooting tab, per-key notes (schema v2). |
| 10-24 | 1 | README archive notice. |
| 11-19 | uncommitted | `CLAUDE.md`, `.claude/`, `okf/`, `scripts/okf-validate.py`, docs in this folder. |

## 3. What is done

### 3.1 Web client (`client/web`)

Verified in code:

| Area | State |
|---|---|
| Connect both halves, auto-connect, hot-plug, side detection | Complete |
| Read all 3 layers (keymap and LEDs) with retries | Complete |
| Key remap, single and multi-select, keyboard and table views | Complete |
| Action palette with search, physical rows, custom HID byte | Complete |
| Tap / Hold / Double / Tap+Hold behaviors | Partial (see 5.1) |
| Per-key LED colour: brush, drag-paint, fill, pipette, custom colours | Complete |
| Per-layer animation (Solid, Breathe, Swirl, Spectrum) | Write-only; device has no read command |
| Idle / sleep / deep-sleep timeouts | Complete |
| Max brightness, scan mode, layer override | Write-only |
| Modules: docked list and gesture table | Read-only; write hidden behind a localStorage flag |
| Devices tab: per-half cards, battery, firmware versions | Complete, read-only |
| Draft queue and Flash dialog with ACK check and re-read | Complete |
| Automatic backup before flash, restore | Complete for keys and LEDs |
| Export and import of keymap and LED JSON | Partial (see 5.1) |
| Per-key notes | Partial (see 5.1) |
| Troubleshooting tab: 12 entries with runnable recipes and a never-send guard | Complete |
| URL state, CDC log panel | Present |

The plan in `docs/superpowers/plans/2026-09-17-openflow-parity.md` is implemented in full except one step (the flavor-diff spike). Its checkboxes were never ticked.

Verification on 2026-11-19: `npm run build` passes, oxlint reports 0 errors and 15 warnings, web smoke 402 ok / 0 FAIL, Python smoke exits 0.

### 3.2 Protocol knowledge (documented)

Recorded as live-tested in `docs/cdc-protocol.md`:

- Frame format, checksum (checked on 269 frames) and multipart reads.
- Keymap read (`30/1003`) and write (`30/1004` with `[00, layer] + record`), 3 layers, record format.
- Record types: HID/consumer keys, momentary layer, output select, Bluetooth/LED/mouse actions, hold-tap, multi-behavior with a shadow slot.
- Length-changing key writes work in both directions.
- LED map read and per-key colour write; effect selection per layer.
- Module presence, type, firmware version and battery voltage; module gesture read and a one-slot write.
- Base and module battery voltage.
- Bootloader: a 2.2 s serial-recovery window, echo and reset, and a software recipe to un-wedge a parked bootloader.
- Recovery of a dark left half, and recovery from a factory format using the vendor app plus a keymap restore.

### 3.3 Tooling and archive

- `toolkit/`: 22 Python scripts. `cdc-client.py` is the core library and CLI. Backup, restore, LED recovery and bootloader un-wedge scripts were used on the device.
- `backup/firmware/`: 15 stock firmware images, all carrying the same signing key hash (re-checked by byte search).
- `research/`: captures, dumps, disassembly, FCC filings.

## 4. What is missing

### 4.1 Features absent from the web client

- Macros.
- Firmware update or downgrade.
- Bluetooth pairing management (only key actions and a read-only name exist).
- More than 3 layers; layer names.
- Keypad keys, shifted or modifier-combined keys, the full consumer-key set.
- "Disabled" and "Transparent" as assignable actions (they are decoded but not offered).
- Layer actions beyond "MO layer 1" and "Hold layer 2".
- Module settings: pointer speed, acceleration, scroll. Gesture editing with the action palette.
- A single "full backup" export; export of module config, timeouts or LED settings.
- Import of the stock NayaFlow backup zip (only a separate Python script builds one).
- Light theme.
- Keyboard-only operation: keycaps are mouse-only.

### 4.2 Protocol unknowns

Listed as open in the docs:

- **Layer-list store.** `30/1002` (write layer list) has no known format. After a factory format (`30/10ca`), hold-to-layer stops working until the vendor app re-flashes. This blocks vendor-free recovery.
- **Right half.** It never answers the `30/10xx` family. How it receives its keymap and colours is unobserved. No right-side recovery exists.
- **Interrupt flavor** wire encoding. The UI stores the choice locally and flashes nothing.
- **Modifier mask on the wire**, which blocks shifted keys.
- **Macros:** the store reads as empty; the write format and whether the firmware executes macros are unknown.
- **Modules:** type code of the Tune module, settings path, config-list write, module firmware update.
- **LED:** layer override (`ed/1014`) shows no effect; no read command for brightness settings; cause of the recurring dark state; stepped animation on the base halves.
- **BLE:** purpose of the custom GATT service; dongle protocol; any configuration over BLE.
- **Battery:** percent formulas are borrowed and lightly calibrated.
- **Command groups CA and F1,** and a range of ED verbs, are unidentified.

### 4.3 Firmware

- All images are signed; the private key is not available. The docs describe buying it from the bankruptcy estate as the only clean path.
- The claim in `docs/firmware-signing.md` that "the update path through the app CDC protocol is already reverse-engineered" is not supported by anything in the repo. No firmware-upload format is documented.
- The bootloader's image-upload group is compiled out. SWD is the only theoretical entry and is untried. The USB MCU is unidentified.
- No tool can re-flash or downgrade stock firmware without NayaFlow.

### 4.4 Project infrastructure

- No LICENSE file. Without one, upstream's code is all-rights-reserved and this fork has no explicit grant to reuse it.
- No test framework, formatter, CONTRIBUTING, issue templates, releases or tags.
- CI builds and deploys only. It runs no lint and no smoke, and has no pull-request trigger.
- Python: no `requirements.txt` or `pyproject.toml`, no version pin, no packaging.
- Every recorded device test was made on the upstream author's unit, vendor app install and macOS rig. The owner of this project has a keyboard, but nothing has been re-verified on it yet.

## 5. What needs fixing

### 5.1 Bugs in the web client (verified)

| # | Problem | Where |
|---|---|---|
| 1 | Tapping Term slider has no effect. The value is ignored and every hold-tap record is written with the 200 ms default. | `src/lib/queue.ts:104`, `src/lib/t10.ts:154-157` |
| 2 | Notes are dropped on import and restore. The parser returns them; `applySnap` never reads them. | `src/lib/importers.ts:112,164`, `src/App.tsx:309-321` |
| 3 | The draft queue lives in memory only. A page reload loses all queued edits. | `src/hooks/useDraft.ts:18` |
| 4 | After a serial reader error, every command just times out; the stored error is never read. | `src/lib/naya.ts:148,163` |
| 5 | A flash cannot be cancelled, and one command can block for about 30 s. | `src/lib/naya.ts:199,239` |
| 6 | Brightness, scan mode and override sliders start at hardcoded values, and touching one queues a write. | `src/components/tabs/BehaviorTab.tsx:88-90` |
| 7 | Settings and module writes are cleared from the queue on ACK alone, although an ACK does not prove the device applied them. | `src/hooks/useFlash.ts:123,136` |
| 8 | A multi-record key write that fails midway leaves the key and its shadow slot inconsistent. | `src/hooks/useFlash.ts:110-117` |
| 9 | Module and timeout reads do not set the busy flag, so background polling can interleave with them. A risk, not an observed failure. | `src/components/tabs/ModulesTab.tsx:91-110`, `src/App.tsx:360` |
| 10 | The read fails hard on any layout other than 156 records and 544 LED bytes per layer; nothing checks the firmware version. | `src/hooks/useLayers.ts:63,72` |
| 11 | Removing the last multi-behavior key does not remove the `4b` tail record. The docs call this test still open. | `src/lib/t10.ts` |

### 5.2 Code health

- 15 oxlint warnings: 11 refs read during render (`App.tsx`, `DevicesTab.tsx`, `useKbFit.ts`), 3 mixed exports in `components/ui`, 1 `Date.now()` in render (`HalfPill.tsx:122`).
- `npm audit`: 2 high. `vite` 8.3.0 (dev-server issues, fixed in 8.3.8) and `source-map-js` (transitive). 22 packages are behind.
- Dead code: `Draft.keyFor`, `Draft.ledFor`, `Draft.has`; four `eslint-disable` comments for a linter that is not installed.
- Duplication: `addCustomColor` twice, LED colouring in two tabs, two near-identical `KeyActionMenu` call sites, two section-label tables with different casing.
- `BindingsTab` takes 37 props. `naya.ts` (1,035 lines) mixes transport, session, parsers and decoders.
- Smoke tooling: the bundle is written to a hardcoded `/tmp/smoke.cjs`; `rolldown` is only a transitive dependency; there is no `npm run smoke` script.
- Untested: every hook (including the flash executor), every component except `Keyboard`, the session beyond connect, import/restore logic.
- Accessibility: no tab roles, no focus trap in the key popover, unlabeled sliders, colour-only status badges.

### 5.3 Toolkit

- `monitor.py` is broken as checked in: it imports from a path in the upstream author's home directory.
- `cdc-client.py` `set`, `ledset` and `raw` write immediately with no dry-run, unlike the other scripts.
- macOS only: ports are `/dev/cu.usbmodem*`, two are hardcoded. No Linux or Windows support.
- `smp-probe4..8.py` reference a `naya-archive` path that no longer exists.
- `toolkit/README.md` says "All tested live", which is not true of the checked-in state.

### 5.4 Stale and contradictory documentation

`docs/cdc-protocol.md` is a chronological lab log. Later sections correct earlier ones in place, so older text is wrong unless read to the end.

- **`fe/100a`:** called a dangerous "commit" early on, later identified as SET ACTIVITY TIMEOUTS. `toolkit/README.md` and `research/README.md` still say "commit".
- **Length-changing writes:** `toolkit/README.md` and the `naya-restore.py` docstring say the device ignores them; the protocol doc marks that refuted.
- **`fa/*`:** the static command map names `fa/1001` "TEST FLASH", yet it is the standard wake probe in every tool. Its real meaning is unresolved.
- **README status table:** lists colour write and module battery as open; both were closed on 09-16.
- **`docs/modules.md`:** a "SOLVED" block is followed by older "STILL OPEN" sections on the same topic.
- **`docs/competitor-gap.md`:** at least five statements were overtaken by later findings.
- **Chip identity:** nRF52810 in one doc, nRF52811 in two others.
- **Inter-half link:** `hardware.md` says there is no radio link between halves; the command map has a "clear all split links" verb.
- **Line 8 of the protocol doc** says messages are CBOR-encoded; they are binary framed.
- **`client/web/README.md`** predates most of the current features.
- **Missing references:** `wire-guard.ts` cites an `AGENTS.md` that does not exist; "UHK #N" tags refer to a list not in the repo; the handoff points to a `naya-create-kb` repo that is not included.
- **The README says the repo is a read-only snapshot,** which is no longer the intent for this fork.

### 5.5 Fork identity

Upstream references to change or decide on:

- `client/web/src/components/Header.tsx:32` links to `github.com/NemeZZiZZ/naya-reflow`.
- `client/web/README.md:7` gives the upstream Pages URL.
- `backup/software/fetch-assets.sh` pulls release assets from the upstream account; `backup/firmware/README.md` describes a third location.
- Root `README.md` archive notice.
- Keep: `tool: 'naya-reflow'` in export files. It is a file-format identifier.

It is unknown whether GitHub Pages is enabled on the fork, and whether the upstream release mirrors still exist.

### 5.6 Legal, privacy and repo size

- **License:** none (see 4.4).
- **Vendor material in git:** 15 proprietary firmware images; a full disassembly of the vendor's NayaCore binary; about 860 action glyphs and fonts extracted from the vendor app, which ship in the deployed site; FCC manuals and lab reports.
- **Privacy:** device serials and BLE addresses appear in docs, dumps and captures. The upstream author's local username and paths appear in two scripts.
- **Secrets:** none found.
- **Size:** `.git` is 219 MB. `research/fcc/` accounts for about 229 MB across 317 files, including PDFs and per-page images of the same pages. No Git LFS.

### 5.7 Device state at handoff (documented, 2026-09-22)

One test unit, base firmware 0.3.41.0. No physical damage recorded; every problem was firmware or settings state.

- Left half and module: working, keymap and colours restored.
- Right half: answering over CDC after a stock flash; backlight not confirmed.
- Open: a cure for the right half's dark state, the brightness-wrap bug, `ed/1014` silence on the right.

## 6. Uncommitted changes from another session

On 2026-11-19 a separate Claude Code session added:

- `okf/`: 26 files in "Open Knowledge Format" v0.2, a condensed restatement of `docs/` and the READMEs. Its log says "Not human-reviewed".
- `scripts/okf-validate.py`, a hook in `.claude/settings.json` that runs it, and a `CLAUDE.md` section telling agents to read `okf/` before device work.

The owner decided on 2026-11-19 that `okf/` is the knowledge base of this project. That makes two things urgent:

- The bundle copies stale statements (the length-change rule, the README's "open" items), and `CLAUDE.md` makes it the first thing read before device work. It needs a review pass against the code.
- It has to be updated in the same change as the code or docs it summarises, or it drifts.

## 7. Not determined

- Which findings create-reflow corrected, and what its SDK and OpenFlow JSON format look like. The repo has no errata list.
- The firmware versions and current state of the owner's own keyboard. The owner has a device (confirmed 2026-11-19); the unit described in 5.7 is the upstream author's.
- Whether Pages and Releases work on `mjhcompany/naya-reflow`.
- Real behaviour of `fa/1001`, `ee/10be` and `ee/10ae`; the firmware-update protocol; whether firmware bodies are really encrypted.
- Not read in full during the audit: several web components, individual troubleshooting entries, the FCC files and binary captures.

See `docs/roadmap-proposal.md` for what to do about all this.
