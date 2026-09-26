<div align="right">

[Русский](./README.ru.md) &nbsp; / &nbsp; **English**

</div>

<p align="center">
  <img src="./docs/media/terra2136-cover-frontier.jpg" width="1200" alt="TERRA 2136 — Desert Stryke. Colonial frontier promotional art.">
</p>

<div align="center">

# TERRA 2136 · Desert Stryke

### Build the line. Take the initiative. Return stronger.

A 3D **tower offense × RTS** with automated squads and collectible battle cards — in a single offline HTML file.

<p>
  <img src="./docs/media/badge-render.svg" height="28" alt="WEBGL 2">
  <img src="./docs/media/badge-format.svg" height="28" alt="SINGLE HTML">
  <img src="./docs/media/badge-play.svg" height="28" alt="OFFLINE">
  <img src="./docs/media/badge-status.svg" height="28" alt="IN DEVELOPMENT">
</p>

</div>

<table width="100%">
<tr><td width="25%" align="center"><h3>50</h3>campaign operations</td><td width="25%" align="center"><h3>82</h3>battle cards</td><td width="25%" align="center"><h3>T1–T6</h3>upgrade tiers</td><td width="25%" align="center"><h3>30</h3>reward days</td></tr>
</table>

---

## 🚀 Quick navigation

| | | |
|---|---|---|
| **[▶ Play](#play)** | Download and launch | Start in 30 seconds |
| **[⚔️ Combat](#combat-loop)** | How battles work | Tactics and strategy |
| **[🎮 Arsenal](#arsenal)** | Units and models | Roles and factions |
| **[📈 Progression](#progression)** | Growth and upgrades | Collections and ranks |
| **[📚 Docs](#documentation)** | Development guides | Technical details |

---

## A strategy game about the front line

TERRA 2136 is built around a simple question: **where should your next resource go — production, defense, an upgrade or a support ability?** You do not micromanage every soldier. Instead, you build the system that produces automated squads, shape the route, and decide when to commit your cards.

The result is a readable mobile RTS with tower-offense pressure: every structure changes the flow of the battlefield, while every operation asks for a different balance between tempo, economy and survival.

<a id="play"></a>

## ▶ Start playing

1. Open the [HTML build](./TERRA2136_PLAY_v0.99.2.html) and select **Download raw file**.
2. Open it in a browser with **WebGL 2**.
3. Choose a deck, enter an operation and build your first production line.

**No installation, account or separate server.** The game is offline and its resources are embedded in the HTML file. On Android, use a browser rather than a document viewer; the game interface is in Russian.

<details><summary><strong>Controls and saves</strong></summary>

**Phone:** tap a pad or structure to select it; drag to pan; pinch to zoom. Select a support ability, then tap a point on the field.

| Action | Keyboard / mouse |
|---|---|
| Select · pan · zoom | Left click · drag · wheel |
| Select a post · open construction | `1` `2` `3` · `B` |
| Card in the construction panel | `Q` `W` `E` `R` `T` `Y` |
| Focus the post · show objectives | `F` · `O` |
| Pause · cancel / close | `Space` · `Esc` |

Progress is stored locally. Settings include **JSON export and import**. On WebGL errors, check browser hardware acceleration.

</details>

<a id="combat-loop"></a>

## ⚔️ Combat mechanics

### How battles work

1. **Build a deck** — Select 6 battle cards and 2 support abilities from your collection.
2. **Choose a post** — Three posts share one route; each post has three construction pads.
3. **Deploy production** — Cards become producers, defenses or tactical tools that shape your lane.
4. **Hold the line** — Automated reinforcements move toward the enemy. Protect the headquarters and contest the central beacon.
5. **Control the tempo** — The beacon generates credits while held; spending too early can leave a gap, while saving too long surrenders the initiative.
6. **Complete the objective** — Hold, break through, escort or evacuate depending on the operation.
7. **Return stronger** — Collect salvage and rewards, improve the collection, tune fittings and prepare the next sortie.

### The tactical layer

| Mechanic | Effect | Strategy |
|---|---|---|
| **Three posts, one front** | Switching attention matters more than unit micromanagement | Control the route, not individual squads |
| **Three pads per post** | Combine production, defense and support roles | Asymmetric builds beat cookie-cutter setups |
| **Automated squads** | Units move and fight without per-unit commands | Focus on composition, timing and positioning |
| **Central beacon** | Holding the centre grants **+6 credits per second** | Beacon control decides the pace of engagement |
| **Population cap** | Powerful formations compete for limited space | Deck variety is forced by design constraints |
| **Support abilities** | Two abilities per operation, used tactically | Save them for breakthrough, defense or siege |

<a id="arsenal"></a>

## 🎮 Arsenal and units

### Unit roles and factions

The battlefield is organized around roles, not copy-paste units:

| Role | Task | Example |
|---|---|---|
| 🪖 **Infantry** | Flexible presence, lane pressure and reliable numbers | Automated squad production |
| 🚗 **Armor** | Durable assault and siege pressure | Siege armor / Pioneer tank |
| 🛩️ **Aircraft** | Fast response and interception | Storm interceptor |
| 🔫 **Defense** | Protect posts and control approaches | Aegis autocannon |
| 🛡️ **Support** | Reinforce positions and deny pushes | Prism ward |

Three faction sets — **Aegis**, **Forge** and **Kairos** — add visual identity and strategic flavor to each deck type.

### Collection and models

Models are not just menu icons: the build includes dedicated 3D unit presentation, faction styling, portraits and hangar inspection. Detail selection adapts to screen size, texture filtering improves legibility, and movement presentation + contact shadows enhance the battlefield clarity.

<table width="100%">
<tr>
  <td width="50%" align="center">
    <img src="./docs/media/arsenal-armor.webp" width="220" alt="Siege armor"><br>
    <strong>Siege armor</strong><br><sub>🔄 ARMOR</sub>
  </td>
  <td width="50%" align="center">
    <img src="./docs/media/arsenal-turret.webp" width="220" alt="Autocannon"><br>
    <strong>Autocannon</strong><br><sub>🔫 DEFENSE</sub>
  </td>
</tr>
<tr>
  <td width="50%" align="center">
    <img src="./docs/media/arsenal-interceptor.webp" width="220" alt="Interceptor"><br>
    <strong>Interceptor</strong><br><sub>🛩️ AIRCRAFT</sub>
  </td>
  <td width="50%" align="center">
    <img src="./docs/media/arsenal-ward.webp" width="220" alt="Defensive ward"><br>
    <strong>Defensive ward</strong><br><sub>🛡️ SUPPORT</sub>
  </td>
</tr>
</table>

### In-game world

<table width="100%">
<tr>
  <td width="50%" align="center">
    <a href="./docs/media/ingame-menu.webp">
      <img src="./docs/media/ingame-menu.webp" width="600" alt="A domed colony in the mountains — headquarters artwork.">
    </a>
    <br><sub>🏛️ Headquarters</sub>
  </td>
  <td width="50%" align="center">
    <a href="./docs/media/ingame-expedition.webp">
      <img src="./docs/media/ingame-expedition.webp" width="600" alt="An expedition beside mineral deposits — in-game artwork.">
    </a>
    <br><sub>🗺️ Expedition</sub>
  </td>
</tr>
</table>

<a id="progression"></a>

## 📈 Progression and upgrades

### Leveling your arsenal

Progression is designed to make sorties feed the next decision:

- 📚 **Card collection** — 82 cards, four rarities and faction sets create different deck directions.
- ⭐ **Experience and ranks** — Repeated use develops the cards you actually play.
- 🎯 **Specializations** — Tune a card toward its preferred role instead of treating copies as identical.
- 🔧 **Modules and fittings** — Save configurations for different operations and switch between damage, defense or economy plans.
- 🏗️ **Structure upgrades** — Battle upgrades run from **T1 to T6**, so a post evolves during a match instead of remaining static.
- 🎁 **Rewards** — Salvage, supply containers, tasks and a 30-day calendar connect campaign sorties with long-term growth.
- 💾 **Local profile** — Progress is stored locally, with JSON export/import for backup and transfer.

### Campaign and game modes

The game includes **50 main operations**, resource missions, a training ground, weekly operations and expedition routes. Objectives change the value of your deck:

| Mode | Objective | Strategy |
|---|---|---|
| 🛡️ **Defend** | Protect the headquarters from waves | Economy-focused deck, sustained output |
| ⚔️ **Breakthrough** | Break through enemy positions | Aggressive, tempo-driven approach |
| 🚚 **Escort** | Protect a convoy or unit | Timing and positioning critical |
| 🏃 **Evacuate** | Extract colonists from danger | Mixed defense and offensive support |

---

<a id="documentation"></a>

## 📚 Documentation and development

**Technology stack:** JavaScript · HTML/CSS · custom WebGL 2 renderer · Fixed-step simulation · Embedded resources · Adaptive resolution

### Getting started

```bash
python3 tools/split.py TERRA2136_PLAY_v0.99.2.html parts/
python3 tools/build.py parts/ dist/TERRA2136_PLAY.html
python3 tools/check.py dist/TERRA2136_PLAY.html
python3 qa/qa.py dist/TERRA2136_PLAY.html --out qa-out --no-battle
```

### Project guides

| Document | Purpose |
|---|---|
| [📄 Build and project structure](./docs/presentation/DEVELOPMENT.md) | Technical architecture and source organization |
| [🗺️ Roadmap](./docs/ROADMAP.md) | Version milestones and release criteria |
| [📝 Changelog](./docs/CHANGELOG.md) | Version history and feature changes |
| [🎨 Media credits](./docs/presentation/MEDIA.md) | Asset sources and attributions |
| [📋 Project rules](./CLAUDE.md) | Development guidelines and invariants |

---

<div align="center">

### One file. Your front line. Your tactics.

Project by [Max-aye](https://github.com/Max-aye) · [Report an issue](https://github.com/Max-aye/TD-RTS---Desert-stryke/issues) · [Play now](./TERRA2136_PLAY_v0.99.2.html)

</div>
