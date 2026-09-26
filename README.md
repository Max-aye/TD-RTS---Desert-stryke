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

[**Play the build ↗**](./TERRA2136_PLAY_v0.99.2.html) · [Quick start](#quick-start) · [Combat](#combat-loop) · [Arsenal](#arsenal) · [Development](#development)

</div>

<table width="100%">
<tr><td width="25%" align="center"><h3>50</h3>campaign operations</td><td width="25%" align="center"><h3>82</h3>battle cards</td><td width="25%" align="center"><h3>T1–T6</h3>upgrade tiers</td><td width="25%" align="center"><h3>30</h3>reward days</td></tr>
</table>

## A strategy game about the front line

TERRA 2136 is built around a simple question: **where should your next resource go — production, defense, an upgrade or a support ability?** You do not micromanage every soldier. Instead, you build the system that produces automated squads, shape the route, and decide when to commit your cards.

The result is a readable mobile RTS with tower-offense pressure: every structure changes the flow of the battlefield, while every operation asks for a different balance between tempo, economy and survival.

<a id="combat-loop"></a>

## How combat works

1. **Build a deck.** Select 6 battle cards and 2 support abilities from your collection.
2. **Choose a post.** Three posts share one route; each post has three construction pads.
3. **Deploy production.** Cards become producers, defenses or tactical tools that shape your lane.
4. **Hold the line.** Automated reinforcements move toward the enemy. Protect the headquarters and contest the central beacon.
5. **Control the tempo.** The beacon generates credits while held; spending too early can leave a gap in the line, while saving too long can surrender the initiative.
6. **Complete the objective.** Hold, break through, escort or evacuate depending on the operation.
7. **Return stronger.** Collect salvage and rewards, improve the collection, tune fittings and prepare the next sortie.

### The tactical layer

- **Three posts, one front:** switching attention between posts matters more than clicking individual units.
- **Three pads per post:** use them to combine production, defense and support rather than stacking one answer everywhere.
- **Automated squads:** the challenge is composition, timing and positioning; the battle remains legible on a phone.
- **Central beacon:** holding the centre funds the push at **+6 credits per second**; losing it accelerates the counter-attack.
- **Population cap:** powerful formations compete for limited space, so a perfect deck is impossible by design.
- **Support abilities:** save them for a breakthrough, emergency defense or a decisive point on the route.

## Unit and model variety

The arsenal combines several battlefield roles rather than a single universal unit:

| Role | Battlefield job | Example |
|---|---|---|
| Infantry | flexible presence, lane pressure and reliable numbers | automated squad production |
| Armor | durable assault and siege pressure | Siege armor / Pioneer tank |
| Aircraft | fast response and interception | Storm interceptor |
| Defense | protects a post and controls an approach | Aegis autocannon |
| Defensive support | reinforces a position or denies a push | Prism ward |

Models are not only menu icons: the build includes dedicated 3D unit presentation, faction styling, portraits and hangar inspection. Detail selection adapts to the unit’s screen size, while texture filtering, movement presentation and contact shadows improve readability during a battle.

The collection is organized around three faction sets — **Aegis, Forge and Kairos** — with four card rarities. Cards can be developed through experience, ranks, specializations, modules and saved fittings, giving the same role room for different builds.

<a id="arsenal"></a>

## Arsenal showcase

<table width="100%"><tr><td width="50%" align="center"><img src="./docs/media/arsenal-armor.webp" width="220" alt="Siege armor"><br><strong>Siege armor</strong><br><sub>ARMOR</sub></td><td width="50%" align="center"><img src="./docs/media/arsenal-turret.webp" width="220" alt="Autocannon"><br><strong>Autocannon</strong><br><sub>DEFENSE</sub></td></tr><tr><td width="50%" align="center"><img src="./docs/media/arsenal-interceptor.webp" width="220" alt="Interceptor"><br><strong>Interceptor</strong><br><sub>AIRCRAFT</sub></td><td width="50%" align="center"><img src="./docs/media/arsenal-ward.webp" width="220" alt="Defensive ward"><br><strong>Defensive ward</strong><br><sub>DEFENSIVE SUPPORT</sub></td></tr></table>

## Progression and upgrades

Progression is designed to make sorties feed the next decision:

- **Card collection:** 82 cards, four rarities and faction sets create different deck directions.
- **Experience and ranks:** repeated use develops the cards you actually play.
- **Specializations:** tune a card toward its preferred tactical role instead of treating every copy as identical.
- **Modules and fittings:** save configurations for different operations and switch from a damage, defense or economy plan.
- **Structure upgrades:** battle upgrades run from **T1 to T6**, so a post can evolve during a match instead of remaining static.
- **Rewards:** salvage, supply containers, tasks and a 30-day calendar connect campaign sorties with long-term growth.
- **Local profile:** progress is stored locally, with JSON export/import for backup and transfer.

## The world of TERRA 2136

<table width="100%"><tr><td width="50%" align="center"><a href="./docs/media/ingame-menu.webp"><img src="./docs/media/ingame-menu.webp" width="600" alt="A domed colony in the mountains — headquarters artwork."></a><br><sub>Headquarters</sub></td><td width="50%" align="center"><a href="./docs/media/ingame-expedition.webp"><img src="./docs/media/ingame-expedition.webp" width="600" alt="An expedition beside mineral deposits — in-game artwork."></a><br><sub>Expedition</sub></td></tr></table>

## Campaign and game modes

The game includes **50 main operations**, resource missions, a training ground, weekly operations and expedition routes. Objectives change the value of your deck: an aggressive breakthrough, a defensive hold and an evacuation demand different production timing and different use of support abilities.

<a id="quick-start"></a>

## Start playing

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

</details>

<a id="development"></a>

## Development

**JavaScript · HTML/CSS · custom WebGL 2 renderer.** Fixed-step simulation, embedded resources, adaptive resolution and portrait/landscape layouts.

[Build and project structure](./docs/presentation/DEVELOPMENT.md) · [Roadmap](./docs/ROADMAP.md) · [Changelog](./docs/CHANGELOG.md) · [Media credits](./docs/presentation/MEDIA.md) · [Project rules](./CLAUDE.md)

```bash
python3 tools/split.py TERRA2136_PLAY_v0.99.2.html parts/
python3 tools/build.py parts/ dist/TERRA2136_PLAY.html
python3 tools/check.py dist/TERRA2136_PLAY.html
python3 qa/qa.py dist/TERRA2136_PLAY.html --out qa-out --no-battle
```

---

<div align="center"><strong>One file. Your front line. Your tactics.</strong><br>Project by <a href="https://github.com/Max-aye">Max-aye</a> · <a href="https://github.com/Max-aye/TD-RTS---Desert-stryke/issues">Report an issue</a></div>
