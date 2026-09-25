<div align="right">

[🇷🇺 Русская версия](./README.ru.md) · [🇬🇧 English version](./README.md)

</div>

<div align="center">

# TERRA 2136 • Desert Stryke

<p><strong>Offline browser tactical RTS / tower offense in one HTML file.</strong></p>

<p>
  <img alt="Status" src="https://img.shields.io/badge/status-v0.99.0%20%2F%20active%20development-0A8F7A?style=for-the-badge" />
  <img alt="Platform" src="https://img.shields.io/badge/platform-browser%20%2F%20offline-FFB703?style=for-the-badge" />
  <img alt="Render" src="https://img.shields.io/badge/render-WebGL2-1E90FF?style=for-the-badge" />
  <img alt="Build" src="https://img.shields.io/badge/build-single%20HTML-E76F51?style=for-the-badge" />
</p>

<p>
  <a href="./index.html">▶ Play now</a> ·
  <a href="./TERRA2136_PLAY_v0.99.0.html">⬇ Playable build v0.99.0</a> ·
  <a href="./docs/ROADMAP.md">🗺 Roadmap</a>
</p>

</div>

---

## Overview

TERRA 2136 is a self-contained tactical strategy game set on a hostile Martian frontier. It combines real-time tower-defense/RTS combat, campaign missions, upgrades, rewards, local progression, responsive mobile-first UI, and WebGL2 rendering. The playable release is a single offline HTML file: no backend, account, CDN, or network connection is required.

## Current release: v0.99.0

The current build includes:

- **Battle HUD 0.96.0:** no battle text below 10 px on tested viewports, touch targets at least 44 px, and a three-step first-battle guide: build → upgrade → support.
- **Unit presentation 0.97.x:** screen-size-based detail selection, an 8× anisotropic-filtering ceiling, acceleration/slope lean, turn banking, and device-scaled model textures.
- **Rewards 0.98.0:** repeat wins pay 35% of the first-clear reward for the first five daily repeats; field alloy finds increased from 3–7 to 6–12.
- **Collection portraits 0.98.1:** dedicated portraits for Grenadier and Missile cards; shared portraits remain only where two loadouts use the same model.
- **Maintenance 0.99.0:** 27 provably dead CSS blocks removed and 36 derived crate-pool tables consolidated into one equivalent table. Simulation, balance, and save format are unchanged.

The full version history is in [`docs/CHANGELOG.md`](./docs/CHANGELOG.md).

## Quick start

### Play immediately

1. Open [`index.html`](./index.html), or open [`TERRA2136_PLAY_v0.99.0.html`](./TERRA2136_PLAY_v0.99.0.html) directly.
2. Start a battle from HQ.
3. Build a defense, upgrade it, use support, and return to HQ to review progression.

### Local preview

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000/>.

## Build and validation

Requirements: Python 3.11+, Node.js 20+, Git, and Playwright for browser QA.

```bash
python3 tools/build.py parts/ dist/TERRA2136_PLAY.html
python3 tools/check.py dist/TERRA2136_PLAY.html

python3 -m pip install playwright
python3 -m playwright install chromium
python3 qa/qa.py dist/TERRA2136_PLAY.html --out qa-out --no-battle
python3 qa/qa.py dist/TERRA2136_PLAY.html --out qa-out --battle-only --viewports mobile
```

Release and regression checks:

```bash
python3 qa/campaign.py TERRA2136_PLAY_v0.99.0.html
python3 qa/perf.py TERRA2136_PLAY_v0.99.0.html
```

The campaign gate passes M01–M05 without console errors. The performance script is a regression comparison running on SwiftShader; the remaining 1.0.0 gate still requires a 30+ FPS measurement on a real phone in a 220-point battle.

## Project structure

```text
.
├── index.html                         # landing page and launch flow
├── TERRA2136_PLAY_v0.99.0.html       # current offline playable build
├── parts/                             # modular source used to build the HTML
│   ├── markup/ css/ ui/               # shell, styles, screens and input
│   ├── game/ engine/ render/           # simulation, runtime and WebGL2 rendering
│   └── data/                          # configuration and embedded assets
├── tools/                             # build, split, checks and analysis tools
├── qa/                                # UI, campaign and performance checks
├── patches/                           # versioned, idempotent patch specifications
└── docs/                              # roadmap, changelog, audit and asset notes
```

## Roadmap

| Version | Focus | Status |
|---|---|---|
| `0.95.0` | HQ order, icons, menu readability | ✅ Complete |
| `0.96.0` | Battle HUD and mobile readability | ✅ Complete |
| `0.97.0` | Unit models, textures and motion | ✅ Complete |
| `0.98.0` | Repeat rewards and field loot | ✅ Complete |
| `0.98.1` | Collection portraits | ✅ Complete |
| `0.99.0` | Styles and technical debt | ✅ Complete |
| `1.0.0` | Release milestone | 🔧 Real-device FPS validation remaining |

See [`docs/ROADMAP.md`](./docs/ROADMAP.md) for acceptance criteria and the phone test procedure.

## Documentation

- [`docs/ROADMAP.md`](./docs/ROADMAP.md) — milestones and release gates
- [`docs/CHANGELOG.md`](./docs/CHANGELOG.md) — version history
- [`docs/AUDIT.md`](./docs/AUDIT.md) — UX and technical audit
- [`docs/ASSETS.md`](./docs/ASSETS.md) — embedded assets and collection portraits
- [`REWARDS_REVIEW.md`](./REWARDS_REVIEW.md) — economy analysis and decisions

---

<div align="center">

[**▶ Open the game**](./index.html) · [**⬇ Playable build**](./TERRA2136_PLAY_v0.99.0.html) · [**🗺 Roadmap**](./docs/ROADMAP.md)

<strong>TERRA 2136 • Desert Stryke</strong>

</div>
