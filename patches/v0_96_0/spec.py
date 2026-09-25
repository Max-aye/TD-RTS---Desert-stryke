"""TERRA 2136 v0.96.0 — battle HUD pass (no simulation, balance or save-format changes).

Anchors come from v0.95.0 and must match exactly. Every edit is presentation:
a 10 px text floor in battle, a 44 px close target in the build panel, and a
first-battle hint that walks through build -> upgrade -> support.
"""
VERSION = '0.96.0'

HINT = 'Строить: ячейка внизу или площадка на карте'

FIRST_RUN_HINT = """/* HUD-096: a player's first battle is a quick battle, where the M01 guide never runs.
 * Steps are read from live simulation facts only: nothing is stored, rewarded or written to the wallet. */
const FIRST_STEPS_096=[
 {text:'1 / 3 · Стройка: ячейка внизу → карта с бойцами',done:s=>s.structures.some(p=>p.team===0)},
 {text:'2 / 3 · Нажмите своё здание → улучшение с ценой',done:s=>s.structures.some(p=>p.team===0&&p.tier>1)},
 {text:'3 / 3 · Поддержка справа внизу → точка на поле',done:s=>Object.values(s.teams[0].cooldowns||{}).some(v=>v>0)}
];
function firstBattleHint096(s){
 if(!s||s.missionId||s.phase!=='battle'||!(meta?.matches===0))return null;
 return FIRST_STEPS_096.find(step=>!step.done(s))?.text||null;
}
"""

EDITS = [
 # --- one version number: tab title, boot line, menu stamp, TERRA_VERSION -------------------
 dict(file='markup/head.html', old='<title>TERRA 2136 · v0.95.0</title>',
      new='<title>TERRA 2136 · v{{VERSION}}</title>', why='tab title still on 0.95.0'),
 dict(file='markup/body.html', old='<small>Офлайн-версия 0.95.0</small>',
      new='<small>Офлайн-версия {{VERSION}}</small>', why='boot screen still on 0.95.0'),
 dict(file='markup/body.html', old='<div class="build-stamp">TERRA 2136 · 0.95.0 · офлайн</div>',
      new='<div class="build-stamp">TERRA 2136 · {{VERSION}} · офлайн</div>', why='menu stamp still on 0.95.0'),
 dict(file='ui/version95.js', old="globalThis.TERRA_VERSION='0.95.0';",
      new="globalThis.TERRA_VERSION='{{VERSION}}';", why='single source of truth for the build number'),

 # --- first battle walks through three steps instead of repeating one line ------------------
 # The anchor carries a marker in 'new', so a second run finds nothing to do instead of inserting twice.
 dict(file='ui/controller.js',
      old="function refreshGuide(){\n if(!sim||screen!=='battle')return;",
      new=FIRST_RUN_HINT + "function refreshGuide(){/* HUD-096 */\n if(!sim||screen!=='battle')return;",
      why='quick battle had no step guidance; the M01 guide only covers the campaign'),
 dict(file='ui/controller.js',
      old=f"  hint.textContent='{HINT}';hint.hidden=!interactive||s.structures.some(p=>p.team===0)||!!cast;",
      new="  const first096=firstBattleHint096(s);\n"
          f"  hint.textContent=first096||'{HINT}';hint.dataset.guide=first096?'true':'false';\n"
          "  hint.hidden=!interactive||!!cast||!$('#quick-upgrade').hidden||(!first096&&s.structures.some(p=>p.team===0));",
      why='the hint disappeared after the first building, before upgrade and support were shown'),
]

NEW_PARTS = [
 dict(file='css/11-hud96.css', source='hud96.css', after='css/10-polish95.css',
      glue_before='</style><style>'),
]
