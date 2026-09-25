#!/usr/bin/env python3
"""Play M01-M05 through the deterministic simulation and watch the console.

    python3 qa/campaign.py GAME.html [--missions M01,M02] [--max-minutes 12]

The release gate for 1.0.0 asks for a full pass of M01-M05 with no console errors.
This drives the real command ledger - it launches each operation, builds a producer
on every post, then advances the simulation in chunks until the match reports a
result. Nothing is stubbed: the same TerraSim that runs on a phone decides the
outcome, so a crash, a validation failure or a stuck objective shows up here.

Frame rate is NOT what this measures. The container renders on SwiftShader, so the
30 FPS clause of the 1.0.0 gate still needs a real device.
"""
import argparse, json, pathlib, sys, time
from playwright.sync_api import sync_playwright

UNLOCK = """(id)=>{
  // Operations gate on the previous clear, so the harness marks earlier ones won.
  // This touches the test profile only; it is not a reward and grants no currency.
  const meta=TerraDebug.meta, order=['M01','M02','M03','M04','M05','M06','M07'];
  for(const prev of order){ if(prev===id) break;
    const row=meta.campaign.missions[prev]; if(row&&!row.wins) row.wins=1; }
  meta.campaign.selectedId=id;
  TerraDebug.setMetaForTest(meta);
  return true;
}"""
LAUNCH = """(id)=>{TerraDebug.start(id);return TerraDebug.state.missionId;}"""
BUILD = """(()=>{
  const s=TerraDebug.state, team=s.teams[0];
  const spawner=team.deck.find(id=>globalThis.TERRA_BALANCE.spawners.find(b=>b.id===id&&(b.kind||'spawner')==='spawner'));
  if(!spawner)return {built:0,reason:'no producer in deck'};
  let built=0;
  for(let lane=0;lane<3;lane++){
    const ack=TerraDebug.command({type:'build',lane,pad:0,blueprint:spawner});
    if(ack&&ack.ok)built++;
  }
  return {built,spawner};
})()"""
STATE = """(()=>{const s=TerraDebug.state;return {tick:s.tick,phase:s.phase,
  hp:[s.teams[0].hp,s.teams[1].hp],winner:s.result?s.result.winner:null,
  reason:s.result?s.result.reason:null,units:s.units.length};})()"""


def run(game, missions, max_minutes):
    report, failures = [], []
    with sync_playwright() as pw:
        b = pw.chromium.launch(args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
        ctx = b.new_context(viewport={'width': 390, 'height': 844}, has_touch=True, is_mobile=True)
        page = ctx.new_page()
        console, errors = [], []
        page.on('console', lambda m: console.append(f'{m.type}: {m.text[:240]}') if m.type == 'error' else None)
        page.on('pageerror', lambda e: errors.append(f'PAGEERROR: {str(e)[:300]}'))
        page.goto(pathlib.Path(game).resolve().as_uri() + '?test=1', wait_until='load', timeout=180000)
        page.wait_for_function("document.getElementById('boot').hidden", timeout=120000)
        time.sleep(1.0)
        page.evaluate("window.__TERRA_MANUAL_FRAME__=true")
        cap = int(max_minutes * 60 * 20)
        for mid in missions:
            before_console, before_errors = len(console), len(errors)
            t0 = time.time()
            page.evaluate(UNLOCK, mid)
            live = page.evaluate(LAUNCH, mid)
            if live != mid:
                failures.append(f'{mid}: did not launch (mission stayed {live})')
            time.sleep(1.0)
            build = page.evaluate(BUILD)
            state = page.evaluate(STATE)
            rebuilds = 0
            while state['phase'] == 'battle' and state['tick'] < cap:
                page.evaluate("(n)=>TerraDebug.step(n)", 400)
                rebuilds += page.evaluate(BUILD).get('built', 0)
                state = page.evaluate(STATE)
            row = {'mission': mid, 'ticks': state['tick'], 'minutes': round(state['tick'] / 20 / 60, 1),
                   'phase': state['phase'], 'winner': state['winner'], 'reason': state['reason'],
                   'built': build.get('built'), 'rebuilt': rebuilds, 'launched': live, 'hp': state['hp'], 'seconds': round(time.time() - t0, 1),
                   'console_errors': console[before_console:], 'page_errors': errors[before_errors:]}
            report.append(row)
            if row['console_errors'] or row['page_errors']:
                failures.append(f"{mid}: {len(row['console_errors'])} console, {len(row['page_errors'])} page errors")
            if state['phase'] == 'battle':
                failures.append(f'{mid}: did not reach a result inside {max_minutes} minutes of simulation')
            print(f"  {mid}: {row['phase']:8s} winner={row['winner']} {row['minutes']:5.1f} min "
                  f"built={row['built']}+{row['rebuilt']} errors={len(row['console_errors']) + len(row['page_errors'])}")
        ctx.close(); b.close()
    out = {'game': pathlib.Path(game).name, 'missions': report, 'problems': failures,
           'result': 'PASS' if not failures else 'FAIL'}
    json.dump(out, open('campaign-report.json', 'w'), ensure_ascii=False, indent=1)
    for p in failures:
        print(' !', p)
    print(f"CAMPAIGN RESULT: {out['result']}")
    return 0 if out['result'] == 'PASS' else 1


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('game')
    ap.add_argument('--missions', default='M01,M02,M03,M04,M05')
    ap.add_argument('--max-minutes', type=float, default=12)
    a = ap.parse_args()
    sys.exit(run(a.game, a.missions.split(','), a.max_minutes))
