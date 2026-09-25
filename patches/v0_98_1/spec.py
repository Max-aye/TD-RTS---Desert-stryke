"""TERRA 2136 v0.98.1 — collection portraits for cards that showed their factory.

Anchors come from v0.98.0 and must match exactly. Presentation only: no simulation,
balance or save-format change.

Measured before the change (tools-side probe over the live collection): 82 cards,
78 distinct pictures, four pairs sharing one. Two of those pairs shared the picture
of the building that produces them - `barracks`/`grenadier` both showed the barracks,
`mortar`/`missile` both showed the factory - even though they field different units.
Those two now show what they actually put on the field.

The other two pairs, `stormInterceptor`/`airBarrage` and `pulseKite`/`pulseSting`,
resolve to the same model in the game data (`storm-interceptor` and `pulse-kite`):
they are two loadouts of one airframe, so a portrait that made them look different
would misrepresent them. docs/ASSETS.md records this.
"""
VERSION = '0.98.1'

EDITS = [
 dict(file='markup/head.html', old='<title>TERRA 2136 · v0.98.0</title>',
      new='<title>TERRA 2136 · v{{VERSION}}</title>', why='tab title still on 0.98.0'),
 dict(file='markup/body.html', old='<small>Офлайн-версия 0.98.0</small>',
      new='<small>Офлайн-версия {{VERSION}}</small>', why='boot screen still on 0.98.0'),
 dict(file='markup/body.html', old='<div class="build-stamp">TERRA 2136 · 0.98.0 · офлайн</div>',
      new='<div class="build-stamp">TERRA 2136 · {{VERSION}} · офлайн</div>', why='menu stamp still on 0.98.0'),
 dict(file='ui/version95.js', old="globalThis.TERRA_VERSION='0.98.0';",
      new="globalThis.TERRA_VERSION='{{VERSION}}';", why='single source of truth for the build number'),

 dict(file='ui/views.js',
      old="function cardImage(ctx,id){if(id==='mortarch')",
      new="function cardImage(ctx,id){/* ASSETS-0981 */"
          "const own981=root.TERRA_ASSETS['card981-'+id+'.webp'];if(own981)return own981;"
          "if(id==='mortarch')",
      why='cards fell through to their production building picture'),
]

NEW_PARTS = [
 dict(file='data/card-previews981.js', source='card-previews981.js',
      after='data/assets-models.js', glue_before='</script><script>'),
]
