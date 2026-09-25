<div align="right">

[🇷🇺 Русская версия](./README.ru.md) <img src="./assets/language-arrow.svg" width="32" alt="переключить язык" /> [🇬🇧 English version](./README.md)

</div>

<div align="center">

# TERRA 2136 • Desert Stryke

<p align="center">
  <img src="./docs/before-after-mobile.png" alt="TERRA 2136 — Desert Stryke" width="900" />
</p>

<p align="center">
  <img alt="Status" src="https://img.shields.io/badge/status-active%20development-0A8F7A?style=for-the-badge" />
  <img alt="Platform" src="https://img.shields.io/badge/platform-browser%20%2F%20offline-FFB703?style=for-the-badge" />
  <img alt="Render" src="https://img.shields.io/badge/render-WebGL2-1E90FF?style=for-the-badge" />
  <img alt="Build" src="https://img.shields.io/badge/build-single%20HTML-E76F51?style=for-the-badge" />
</p>

### Offline browser strategy prototype with a full game loop, UI systems, and QA automation

A self-contained tactical RTS built in a single HTML file. The project focuses on a clean gameplay loop, mobile-first UX, strong visual identity, and maintainable architecture without external dependencies.

<p align="center">
  <a href="./index.html"><img src="https://img.shields.io/badge/▶%20Play%20Now-FFD166?style=for-the-badge&logo=play&logoColor=111827" alt="Play now" /></a>
  <a href="./TERRA2136_PLAY_v0.99.1.html"><img src="https://img.shields.io/badge/⬇%20Playable%20Build-v0.99.1-7AE582?style=for-the-badge" alt="Playable build" /></a>
  <a href="./docs/ROADMAP.md"><img src="https://img.shields.io/badge/🗺%20Roadmap-9AA0FF?style=for-the-badge" alt="Roadmap" /></a>
</p>

</div>

---

## Overview

TERRA 2136 is a compact tactical strategy prototype set on a hostile Martian frontier. The game combines:

- real-time tower defense / RTS combat;
- campaign progression and map progression;
- modular upgrades, rewards, and player systems;
- mobile-first interface design and responsive layouts;
- WebGL2 rendering with a single offline build.

This project was designed as both a playable game and a technical showcase: it demonstrates how to structure a browser game with split source files, deterministic simulation logic, UI engineering, and QA validation within a single repository.

---

## Why this project stands out

| Area | What it demonstrates |
|---|---|
| Gameplay systems | Tactical combat, resource flow, progression, and decision-making under time pressure |
| Architecture | Split source structure rebuilt into one distributable HTML artifact |
| UI / UX | Mobile-first interface, readable controls, compact action loops, and screen flow |
| Technical quality | QA automation, script validation, and repeatable build workflows |
| Presentation | Distinct visual identity and polished public-facing project page |

---

## Quick start

### Play immediately

1. Open [`index.html`](./index.html).
2. Launch the game from the landing page.
3. Or run the bundled build directly: [`TERRA2136_PLAY_v0.99.1.html`](./TERRA2136_PLAY_v0.99.1.html).

No back-end, account system, or external CDN is required.

### Local HTTP preview

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000/>.

---

## Project structure

```text
.
├── index.html                        # landing / launch page
├── TERRA2136_PLAY_v0.99.1.html       # playable offline build
├── parts/                            # source files used to rebuild the game
│   ├── markup/                      # HTML shell, battle screen, menu frames
│   ├── css/                         # UI styling layers and polish rules
│   ├── ui/                          # navigation, screens, HUD, input logic
│   ├── game/                        # simulation, campaign logic, progression
│   ├── render/                      # render pipeline and visual effects
│   ├── engine/                      # runtime and game loop infrastructure
│   └── data/                        # configuration, assets, embedded resources
├── tools/                            # split, build, syntax-check, patch utilities
├── qa/                               # automated UI and smoke-test validation
├── patches/                          # versioned patch workflow and revision history
├── docs/                             # roadmap, changelog, audit, game notes
├── CLAUDE.md                         # project rules and invariants
├── PROMPTS.md                        # task framing and goal templates
├── REWARDS_REVIEW.md                 # economy and reward analysis
├── README.md                         # English project overview
├── README.ru.md                      # Russian project overview
├── .github/                          # GitHub workflow and repository config
└── .claude/                          # local assistant/project guidance files
```

---

## Technical highlights

### Game systems

- deterministic battle simulation with fixed-step logic;
- campaign flow, progression, and mission structure;
- local persistence and resource transactions;
- mobile-first UI with responsive behavior for different screen sizes;
- single-file offline delivery without external runtime dependencies.

### Engineering discipline

- source split into modular parts before final build;
- automated syntax checks through `node --check`;
- Playwright-based interface validation and smoke tests;
- versioned patch workflow for controlled iteration;
- documentation-first development with design notes and roadmap tracking.

---

## Build and validation

### Requirements

- Python 3.11+
- Node.js 20+
- Git
- Playwright for UI automation

### Build the game

```bash
python3 tools/build.py parts/ dist/TERRA2136_PLAY.html
```

### Rebuild from a split HTML file

```bash
python3 tools/split.py TERRA2136_PLAY_v0.99.1.html parts/
```

### Syntax validation

```bash
python3 tools/check.py dist/TERRA2136_PLAY.html
```

### UI QA / smoke test

```bash
python3 -m pip install playwright
python3 -m playwright install chromium

python3 qa/qa.py dist/TERRA2136_PLAY.html --out qa-out --no-battle
python3 qa/qa.py dist/TERRA2136_PLAY.html --out qa-out --battle-only --viewports mobile
```

This validates menu flow, touch targets, overflow, visual readability, and battle startup stability.

---

## Roadmap

| Version | Focus | Status |
|---|---|---|
| `0.95.0` | UI clarity, icons, layout polish | ✅ Complete |
| `0.96.0` | Combat HUD improvements | ✅ Complete |
| `0.97.0` | Unit models: detail, textures, motion | ✅ Complete |
| `0.98.0` | Reward progression tuning | ✅ Complete |
| `0.98.1` | Collection portraits | ✅ Complete |
| `0.99.0` | Styles and tech debt | ✅ Complete |
| `1.0.0` | Release | 🔧 Planned |
| `0.98.1` | Map visual polish | 🗺️ Planned |
| `1.0.0` | Release-ready milestone | 🎯 Target |

See [`docs/ROADMAP.md`](./docs/ROADMAP.md) for detailed milestones.

---

## Documentation

- [`docs/ROADMAP.md`](./docs/ROADMAP.md) — project route and release planning
- [`docs/CHANGELOG.md`](./docs/CHANGELOG.md) — version history and updates
- [`docs/AUDIT.md`](./docs/AUDIT.md) — UX and technical audit
- [`docs/REWARDS_REVIEW.md`](./docs/REWARDS_REVIEW.md) — economy and progression analysis
- [`docs/RESEARCH_NOTES.md`](./docs/RESEARCH_NOTES.md) — research and design notes
- [`CLAUDE.md`](./CLAUDE.md) — development rules and invariants
- [`PROMPTS.md`](./PROMPTS.md) — task framing and execution patterns

---

## Portfolio angle

This project is a strong portfolio example because it combines gameplay design and software engineering in a compact, demonstrable package:

- playable and testable browser game;
- clear code structure and build pipeline;
- systems thinking across UI, progression, and logic;
- attention to UX and readability;
- automated verification instead of assumptions.

It is especially suitable for discussing software craftsmanship, product iteration, and building a game from a focused prototype to a more polished experience.

---

<div align="center">

### Explore the project

[**▶ Open the game**](./index.html) · [**⬇ Playable build**](./TERRA2136_PLAY_v0.99.1.html) · [**🗺 Roadmap**](./docs/ROADMAP.md)

<br>

<strong>TERRA 2136 • Desert Stryke</strong>

</div>
