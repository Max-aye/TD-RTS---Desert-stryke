"""TERRA 2136 v0.95.0 — presentation pass (no simulation, balance or save-format changes).

Each EDIT names the problem it fixes. Anchors come from v0.94.0 and must match exactly.
"""
VERSION = '0.95.0'

HINT_OLD = 'Пост → карта · враг виден в обзоре'
HINT_NEW = 'Строить: ячейка внизу или площадка на карте'

EDITS = [
 # --- head: favicon, app icon, one version in the tab title -------------------------------
 dict(file='markup/head.html',
      old='<link rel="icon" href="data:,"><title>TERRA 2136 · v0.90.0 · Мортарх</title>',
      new='<link rel="icon" href="{{FILE:favicon.uri}}"><link rel="apple-touch-icon" href="{{FILE:apple-touch.uri}}">'
          '<meta name="description" content="TERRA 2136 — офлайн tower offense: стройте посты, выпускайте отряды, удерживайте рубеж.">'
          '<title>TERRA 2136 · v{{VERSION}}</title>',
      why='empty favicon, stale title v0.90.0'),
 # --- boot + menu markup ---------------------------------------------------------------------
 dict(file='markup/body.html', old='<div class="brand-mark">T<span>◈</span></div>',
      new='<div class="brand-mark brand-mark95">{{FILE:emblem.svg}}</div>', why='drawn brand emblem on boot'),
 dict(file='markup/body.html', old='<small>OFFLINE BUILD · 0.77.0</small>',
      new='<small>Офлайн-версия {{VERSION}}</small>', why='boot showed 0.77.0'),
 dict(file='markup/body.html', old='<div class="build-stamp">ПРОТОТИП 0.77.0 · VISUAL MERGE · БЕЗ СЕТИ</div>',
      new='<div class="build-stamp">TERRA 2136 · {{VERSION}} · офлайн</div>', why='menu stamp showed 0.77.0 and dev jargon'),
 dict(file='markup/body.html', old=f'<div id="battle-hint">{HINT_OLD}</div>',
      new=f'<div id="battle-hint">{HINT_NEW}</div>', why='cryptic battle hint (markup)'),
 dict(file='ui/controller.js', old=f"'{HINT_OLD}'", new=f"'{HINT_NEW}'", count=3,
      why='cryptic battle hint (prewarm + guide reset)'),
 # --- HQ information order -------------------------------------------------------------------
 dict(file='ui/controller.js',
      old="""(m.querySelector('.hq-primary')||m.firstElementChild)?.insertAdjacentHTML('beforeend',AfterUI.action(ctx(),reportArchive));
 if(!guide.everCompleted){const entry=m.querySelector('.hq-primary')||m.querySelector('.hq09')||m.firstElementChild;if(entry)entry.insertAdjacentHTML('beforeend',GuideUI.entry(guideContext()));}""",
      new="""/* HQ-095: .hq-primary no longer exists, so reports + tutorial were injected into the AGI card and
    squeezed to a 42 px column. Fixed order: next step (AGI) -> launch -> long tracks -> utilities. */
 {const home=m.querySelector('.command-home'),tracks=document.createElement('div'),utility=document.createElement('div');
  tracks.className='hq-tracks95';utility.className='hq-utility95';
  m.querySelectorAll(':scope>.j88-entry,:scope>.e89-entry').forEach(n=>tracks.append(n));
  utility.insertAdjacentHTML('beforeend',AfterUI.action(ctx(),reportArchive));
  if(!guide.everCompleted)utility.insertAdjacentHTML('beforeend',GuideUI.entry(guideContext()));
  if(home)home.after(tracks,utility);else m.append(tracks,utility);
  if(!tracks.childElementCount)tracks.remove();if(!utility.childElementCount)utility.remove();}""",
      why='HQ layout bug + launch below the fold'),
 # --- one nav icon family --------------------------------------------------------------------
 dict(file='ui/controller.js',
      old="""aria-current="${route===id?'page':'false'}">${I(ic)}<span>${n}</span></button>`""",
      new="""aria-current="${route===id?'page':'false'}">${globalThis.TerraIcons95?.svg(ic)||I(ic)}<span>${n}</span></button>`""",
      why='nav mixed line icons with raster art'),
 # --- versions, player-facing copy -----------------------------------------------------------
 dict(file='ui/controller.js', old="const report={version:'0.77.0',", new="const report={version:globalThis.TERRA_VERSION,",
      why='device report version'),
 dict(file='ui/controller.js', old="window.TerraHealth=()=>({version:'0.90.0',", new="window.TerraHealth=()=>({version:globalThis.TERRA_VERSION,",
      why='health probe version'),
 dict(file='ui/controller.js', old='Версия 0.77.0 · EMERALD FRONTIER. Три визуальные фракции,',
      new='Версия ${globalThis.TERRA_VERSION}. Три фракции,', why='settings showed 0.77.0'),
 dict(file='ui/controller.js',
      old="'Автосохранение использует отдельное хранилище прототипа. Сохранения ARK не изменяются.'",
      new="'Прогресс сохраняется автоматически на этом устройстве. Для переноса на другое устройство используйте экспорт JSON.'",
      why='developer jargon in settings'),
 dict(file='ui/controller.js', old="['emperor','Emperor · '", new="['emperor','Император · '", why='English label in hangar filters'),
]

NEW_PARTS = [
 dict(file='ui/version95.js', source='version95.js', after='ui/views.js'),
 dict(file='ui/icons95.js', source='icons95.js', after='ui/version95.js'),
 dict(file='css/10-polish95.css', source='polish95.css', after='css/09-guide91.css', glue_before='</style><style>'),
]
