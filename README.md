<div align="right">

[Русский](./README.ru.md) &nbsp; / &nbsp; **English**

</div>

<p align="center">
  <img src="./docs/screen-battle.png" width="600" alt="TERRA 2136 — Desert Stryke. Live operation on a phone.">
</p>

<div align="center">

# TERRA 2136 · Desert Stryke

### Build the line. Take the initiative. Return stronger.

A 3D **tower offense × RTS** with automated squads
and collectible battle cards — in a single HTML file.

[**Game build ↗**](./TERRA2136_PLAY_v0.99.2.html) &nbsp; · &nbsp; [Quick start](#quick-start) &nbsp; · &nbsp; [Arsenal](#arsenal) &nbsp; · &nbsp; [Development](#development)

</div>

<table width="100%">
  <tr>
    <td width="25%" align="center"><h3>50</h3>campaign operations</td>
    <td width="25%" align="center"><h3>82</h3>battle cards</td>
    <td width="25%" align="center"><h3>T1–T6</h3>battle upgrades</td>
    <td width="25%" align="center"><h3>30</h3>days of rewards</td>
  </tr>
</table>

## Tactics over micromanagement

Build production and defenses along a shared route. Three posts with three building pads each, automated reinforcements and a central beacon turn every battle into a contest of timing and position.

Choose a deck of **6 cards and 2 support abilities**. Protect headquarters, break through defenses or evacuate colonists — each operation changes the objective.

<p align="center"><strong>Deck → deploy → battle → rewards → upgrades</strong></p>

## Every sortie strengthens your arsenal

- **Campaign and sorties:** 50 main operations, resource missions, a training ground, weekly operations and expedition routes.
- **Collection and progression:** four card rarities, experience, ranks, specializations, modules and saved fittings.
- **Rewards through play:** battlefield salvage, supply containers, tasks and a 30-day reward calendar.
- **Headquarters and hangar:** deck building, model inspection, upgrade planning and after-action reports.

<a id="arsenal"></a>

## Build your arsenal

Infantry, armor, aircraft and defensive structures. **Aegis · Forge · Kairos** — three faction sets for your front line.

<a id="quick-start"></a>

## Start playing

1. Open the [HTML build](./TERRA2136_PLAY_v0.99.2.html) and select **Download raw file**.
2. Open the downloaded file in a browser with **WebGL 2**.
3. Choose a deck and launch your first operation.

**No installation, account or separate server.** All game resources are included. On Android, open the HTML in a browser rather than a document viewer. The game interface is in Russian.

<details>
<summary><strong>Controls and saves</strong></summary>

**Phone:** tap a pad or structure to select it; drag to pan; pinch to zoom. Select a support ability, then tap a point on the field.

| Action | Keyboard / mouse |
| --- | --- |
| Select · pan · zoom | Left click · drag · wheel |
| Select a post · open construction | `1` `2` `3` · `B` |
| Card in the open construction panel | `Q` `W` `E` `R` `T` `Y` |
| Focus the post · show objectives | `F` · `O` |
| Pause · cancel / close | `Space` · `Esc` |

Letter shortcuts use an English keyboard layout.

Progress is stored locally. Settings include **JSON export and import**. Import replaces the current profile with the selected snapshot — export a backup first.

For WebGL errors, check browser hardware acceleration. On slower devices, lower quality and battle size. Local opening and storage on Android depend on the browser.

</details>

<a id="development"></a>

## Development

**JavaScript · HTML/CSS · custom WebGL 2 renderer.**
Fixed-step simulation, embedded resources, adaptive resolution, and portrait and landscape layouts.

[Build and project structure](./docs/presentation/DEVELOPMENT.md) · [Roadmap](./docs/ROADMAP.md) · [Changelog](./docs/CHANGELOG.md) · [Project rules](./CLAUDE.md)

### Toolchain

```bash
python3 tools/split.py TERRA2136_PLAY_v0.99.2.html parts/
python3 tools/build.py parts/ dist/TERRA2136_PLAY.html
python3 tools/check.py dist/TERRA2136_PLAY.html
python3 qa/qa.py dist/TERRA2136_PLAY.html --out qa-out --no-battle
python3 qa/qa.py dist/TERRA2136_PLAY.html --out qa-out --battle-only --viewports mobile
```

On Windows, replace `python3` with `py`.

---

<div align="center">

**One file. Your front line. Your tactics.**

Project by **[Max-aye](https://github.com/Max-aye)** · [Report an issue](https://github.com/Max-aye/TD-RTS---Desert-stryke/issues)

</div>
