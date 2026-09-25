"""TERRA 2136 v0.99.0 — стили и техдолг.

Anchors come from v0.98.1 and must match exactly. Nothing here changes what the game
looks like or how it plays; both changes are provable equivalences.

1. `css/00-base.css`. The sheet stacks style layers from many versions, so the same
   selector is declared again and again - 639 selectors repeat. Most of those repeats
   live in different @media contexts and are load-bearing. Only 27 blocks are provably
   dead: same selector, same @media context, and a later block re-declares every
   property, so source order settles it. Those 27 are removed here, one edit each, and
   `tools/cssdedupe.py` reproduces the list. Screenshots of all five menu routes plus
   settings, on 390x844 and 1440x900, match v0.98.1 to within 0.001% of pixels.

2. Crate pools. Thirty-six tables (CRATE_POOLS28..CRATE_POOLS90) derived each from the
   previous one; only CRATE_POOLS90 is read at runtime, by cratePolicy. They collapse
   into a single literal table with the same 37 policies - verified byte-identical after
   JSON round-trip - and the per-version history is kept as a provenance comment, so a
   save still draws from exactly the pool it was written against.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
VERSION = '0.99.0'

EDITS = [
 dict(file='markup/head.html', old='<title>TERRA 2136 · v0.98.1</title>',
      new='<title>TERRA 2136 · v{{VERSION}}</title>', why='tab title still on 0.98.1'),
 dict(file='markup/body.html', old='<small>Офлайн-версия 0.98.1</small>',
      new='<small>Офлайн-версия {{VERSION}}</small>', why='boot screen still on 0.98.1'),
 dict(file='markup/body.html', old='<div class="build-stamp">TERRA 2136 · 0.98.1 · офлайн</div>',
      new='<div class="build-stamp">TERRA 2136 · {{VERSION}} · офлайн</div>', why='menu stamp still on 0.98.1'),
 dict(file='ui/version95.js', old="globalThis.TERRA_VERSION='0.98.1';",
      new="globalThis.TERRA_VERSION='{{VERSION}}';", why='single source of truth for the build number'),

 dict(file='game/progress.js',
      old=open(os.path.join(HERE, 'crate-chain.old.txt'), encoding='utf-8').read(),
      new=open(os.path.join(HERE, 'crate-table.new.txt'), encoding='utf-8').read(),
      why='36 derived crate tables collapse into one, same 37 policies'),
]

# 27 stylesheet blocks a later rule in the same context fully overrides
for _e in json.load(open(os.path.join(HERE, 'css-dead.json'), encoding='utf-8')):
    EDITS.append(dict(file='css/00-base.css', old=_e['old'], new=_e['new'],
                      why='dead duplicate: ' + _e['why']))
