#!/usr/bin/env python3
"""First-week economy model for the "new player, 3 battles a day" profile.

    python3 tools/economy.py [parts]

Reads the shipped numbers - TERRA_PROGRESSION.daily, the campaign reward table and
TERRA_LOOT_CONFIG - and prints where a new player's alloy comes from in week one.
The roadmap target for 0.98.0 is a battle share of at least 60%.

The model is deliberately explicit; every assumption is printed with the result:
  * three battles a day for seven days;
  * at most NEW_OPS_PER_DAY fresh operations a day - a new player does not clear
    twenty-one operations in week one - and every other battle is a repeat, which
    is the source the rewards review calls weak;
  * expected field loot per battle from TERRA_LOOT_CONFIG weights and an assumed
    drop count, well under the 28 cap;
  * crates and blueprints are left out of the alloy totals - they hand out cards,
    not currency - and are reported separately.
"""
import json, re, sys, pathlib

PARTS = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'parts')
BATTLES_PER_DAY = 3
DAYS = 7
DROPS_PER_BATTLE = 12        # typical clear, far below maxDropsPerBattle
NEW_OPS_PER_DAY = 1          # pessimistic: one fresh operation a day, the rest repeats
REPEAT_CAP_DEFAULT = None    # set by the repeat policy read from progress.js


def load_progression():
    text = (PARTS / 'data/design-config.js').read_text(encoding='utf-8')
    start = text.index('window.TERRA_PROGRESSION=')
    body = text[text.index('{', start):]
    depth = 0
    for i, ch in enumerate(body):
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if not depth:
                return json.loads(body[:i + 1])
    raise SystemExit('TERRA_PROGRESSION not found')


def load_loot():
    text = (PARTS / 'data/design-config.js').read_text(encoding='utf-8')
    start = text.index('window.TERRA_LOOT_CONFIG=')
    body = text[text.index('{', start):]
    depth = 0
    for i, ch in enumerate(body):
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if not depth:
                return json.loads(body[:i + 1])
    raise SystemExit('TERRA_LOOT_CONFIG not found')


def load_missions():
    """The campaign table is JS object literals, so read the fields by pattern."""
    text = (PARTS / 'game/content-sim.js').read_text(encoding='utf-8')
    out = []
    for m in re.finditer(r"\{id:'(M\d\d)'", text):
        chunk = text[m.start():m.start() + 2600]
        rec = {'id': m.group(1)}
        for key in ('reward', 'repeat'):
            g = re.search(key + r':\{([^}]*)\}', chunk)
            rec[key] = {}
            if g:
                for pair in re.finditer(r"(\w+):(\d+)", g.group(1)):
                    rec[key][pair.group(1)] = int(pair.group(2))
        if rec['reward']:
            out.append(rec)
    seen, unique = set(), []
    for r in out:
        if r['id'] in seen:
            continue
        seen.add(r['id'])
        unique.append(r)
    unique.sort(key=lambda r: r['id'])
    return unique


def repeat_policy():
    """R1 ships as a formula in progress.js, so read the live rule, not a guess."""
    text = (PARTS / 'game/progress.js').read_text(encoding='utf-8')
    share = re.search(r'REPEAT_SHARE_098\s*=\s*([\d.]+)', text)
    cap = re.search(r'REPEAT_CAP_098\s*=\s*(\d+)', text)
    return (float(share.group(1)) if share else None, int(cap.group(1)) if cap else None)


def loot_alloy_per_battle(loot):
    total = sum(t['weight'] for t in loot['types'])
    alloy = next(t for t in loot['types'] if t['id'] == 'alloy')
    mean = (alloy['min'] + alloy['max']) / 2
    return DROPS_PER_BATTLE * (alloy['weight'] / total) * mean


def run():
    prog, loot, missions = load_progression(), load_loot(), load_missions()
    share, cap = repeat_policy()
    per_battle_loot = loot_alloy_per_battle(loot)

    cleared, first_alloy, repeat_alloy, loot_alloy, gift_alloy = [], 0, 0, 0, 0
    crates = {'battle': 0, 'gift': 0}
    for day in range(1, DAYS + 1):
        gift = prog['daily'][day - 1]
        gift_alloy += gift.get('alloy', 0)
        if gift.get('crate'):
            crates['gift'] += 1
        repeats_today, new_today = 0, 0
        for _ in range(BATTLES_PER_DAY):
            loot_alloy += per_battle_loot
            nxt = next((m for m in missions if m['id'] not in cleared), None) if new_today < NEW_OPS_PER_DAY else None
            if nxt:
                new_today += 1
                first_alloy += nxt['reward'].get('alloy', 0)
                cleared.append(nxt['id'])
                continue
            best = missions[len(cleared) - 1]
            if share is not None:
                allowed = cap is None or repeats_today < cap
                gain = round(best['reward'].get('alloy', 0) * share) if allowed else best['repeat'].get('alloy', 0)
            else:
                gain = best['repeat'].get('alloy', 0)
            repeat_alloy += gain
            repeats_today += 1

    battle = first_alloy + repeat_alloy + loot_alloy
    total = battle + gift_alloy
    pct = battle / total * 100 if total else 0
    print(f'profile: new player, {BATTLES_PER_DAY} battles/day, {DAYS} days, {DROPS_PER_BATTLE} drops/battle, {NEW_OPS_PER_DAY} new op/day')
    print(f'repeat policy: ' + (f'{share:.0%} of the first win, cap {cap}/day' if share is not None else 'fixed table value'))
    print(f'  first wins   {first_alloy:8.0f} alloy  ({len(cleared)} operations)')
    print(f'  repeats      {repeat_alloy:8.0f} alloy')
    print(f'  field loot   {loot_alloy:8.0f} alloy')
    print(f'  daily gifts  {gift_alloy:8.0f} alloy  ({crates["gift"]} crates)')
    print(f'  battle share {pct:8.1f}%  (target >= 60%)')
    print('BATTLE SHARE: PASS' if pct >= 60 else 'BATTLE SHARE: FAIL')
    return 0 if pct >= 60 else 1


if __name__ == '__main__':
    sys.exit(run())
