<div align="right">

[🇷🇺 Русская версия](./README.ru.md) · [🇬🇧 English](./README.md)

</div>

<div align="center">

# TERRA 2136 · Desert Stryke

### Hold the line on a dead frontier — a whole RTS in one offline HTML file

<p>
  <img alt="Version" src="https://img.shields.io/badge/version-0.99.2-0A8F7A?style=for-the-badge" />
  <img alt="Platform" src="https://img.shields.io/badge/platform-browser%20·%20offline-FFB703?style=for-the-badge" />
  <img alt="Render" src="https://img.shields.io/badge/render-WebGL2-1E90FF?style=for-the-badge" />
  <img alt="Build" src="https://img.shields.io/badge/build-single%20HTML-E76F51?style=for-the-badge" />
  <img alt="Dependencies" src="https://img.shields.io/badge/runtime%20dependencies-0-8A6FE8?style=for-the-badge" />
</p>

<p>
  <a href="./TERRA2136_PLAY_v0.99.2.html"><b>⬇ Download and play</b></a> ·
  <a href="./index.html">▶ Launch page</a> ·
  <a href="./docs/ROADMAP.md">🗺 Roadmap</a> ·
  <a href="./docs/CHANGELOG.md">📓 Changelog</a>
</p>

<img src="./docs/screen-battle.png" width="270" alt="Battle on a phone" />
<img src="./docs/screen-boot.png" width="270" alt="Loading screen" />

<sub>Left: a live operation on a 390 px phone. Right: the boot sequence.</sub>

</div>

---

## One file. No server. No network.

Download `TERRA2136_PLAY_v0.99.2.html`, open it, play. That is the whole install.

No backend, no account, no CDN, no analytics, no build step for the player. Every model,
texture, icon and sound cue is embedded in the document. Put it on a phone in airplane
mode and it still runs — **43 MB of game in a single `.html`**.

```
open TERRA2136_PLAY_v0.99.2.html      # that's it
```

## The game

A tower-offense / RTS hybrid on a hostile Martian frontier. You do not command units
directly — you build the machine that produces them, and the line holds or it does not.

- **Three posts, one front.** Pick a post, build a producer, upgrade it under fire.
  Every card is a building that keeps sending troops down the road.
- **The beacon pays.** Hold the centre and it funds you at +6 credits a second.
  Lose it and the counter-attack is already walking.
- **Real decisions, not menus.** Six deck slots, two support abilities, six upgrade
  tiers per structure, and a fixed population cap — you cannot have everything.
- **50 campaign operations**, 82 cards across four rarities, expeditions, a 30-day
  calendar, modules, technologies, field salvage and a terminal.
- **Built for a phone first.** 390 px portrait is the design target, not an afterthought:
  10 px text floor, 44 px touch targets, adaptive resolution under load.

## Under the hood

This is also an engineering exercise, and the constraints are the interesting part.

| | |
|---|---|
| **Deterministic simulation** | Fixed 20 Hz step, seeded RNG, no wall-clock reads in gameplay. The same seed and the same commands always produce the same match — which is what makes the save format and the automated campaign gate possible. |
| **Render is never authoritative** | Presentation modules may read simulation state, never write it. Body lean, bank, detail selection and contact shadows all live on render-side actors. |
| **Transactional economy** | The wallet only changes through `TerraProgress` candidate → write → accept. The UI never grants anything to itself. |
| **Versioned policies, not rewrites** | Crate pools and the terminal payout table are versioned, and saves carry which version paid them. A five-year-old profile still validates receipt by receipt. |
| **Split sources, rebuilt output** | Nobody edits the 43 MB file. It is split into `parts/`, edited there, and rebuilt — with a byte-identical round trip as the proof the split is lossless. |

## Toolchain

The repository ships the tools it is developed with. Every one of them prints a verdict.

| Command | What it proves |
|---|---|
| `python3 tools/split.py GAME.html parts/` | Break the build into editable sources |
| `python3 tools/build.py parts/ dist/GAME.html --verify` | Reassemble; `--verify` asserts a byte-identical round trip |
| `python3 tools/patch.py patches/vX_Y_Z parts/` | Apply a versioned patch set — all of it or none of it, and idempotent |
| `python3 tools/check.py GAME.html` | `node --check` over every embedded script block |
| `python3 qa/qa.py GAME.html --out qa-out` | Headless tour of menu and battle: broken images, overflow, tiny text, small tap targets, dock stability |
| `python3 qa/campaign.py GAME.html` | Plays M01–M05 through the real simulation and fails on any console error |
| `python3 qa/perf.py GAME.html` | CPU cost per simulated tick in a 220-point battle, compared against a stored baseline |
| `python3 tools/economy.py` | Where a new player's income actually comes from in week one |
| `python3 tools/cssdedupe.py parts/css/00-base.css` | Finds style blocks a later rule provably overrides |

Patch sets are the unit of change. Each one names the problem it fixes, matches its
anchors exactly, and refuses to write anything if a single anchor moved — so a patch
either lands whole or tells you why it cannot.

## Repository layout

```
TERRA2136_PLAY_v0.99.2.html   the game — one file, offline
index.html                    landing page
parts/                        editable sources (generated by split.py, not committed)
patches/vX_Y_Z/               versioned patch sets, one folder per release
tools/                        split, build, patch, check, economy, cssdedupe
qa/                           headless QA, campaign gate, performance gauge
docs/                         roadmap, changelog, audit, assets, research notes
CLAUDE.md                     project rules: source map, invariants, review standards
```

## Status

**v0.99.2.** Every roadmap milestone up to 1.0.0 is closed and measured: battle HUD
readability, unit model detail and motion, reward economy, collection art, style and
tech debt, terminal policy, boot sequence.

One release criterion remains, and it needs hardware rather than code: **30+ FPS in a
220-point battle on a real phone.** This repository's CI renders on SwiftShader without
a GPU, so no number produced here can answer it. The procedure is in
[`docs/ROADMAP.md`](./docs/ROADMAP.md).

## Requirements

Playing needs a WebGL2 browser and nothing else. Developing needs Python 3.11+, Node 20+,
and Playwright for the QA scripts:

```bash
python3 -m pip install playwright && python3 -m playwright install chromium
```

---

<div align="center">

**[⬇ Download the game](./TERRA2136_PLAY_v0.99.2.html)** · **[🗺 Roadmap](./docs/ROADMAP.md)** · **[📓 Changelog](./docs/CHANGELOG.md)**

<sub>Development repository and working copy of TERRA 2136 · Desert Stryke.</sub>

</div>
