#!/usr/bin/env python3
"""TERRA 2136 headless QA: menu tour, UI lint, battle smoke test.

    python3 qa/qa.py GAME.html --out qa-out [--viewports mobile,desktop] [--battle-seconds 20]

Exit code 0 only when: no page errors, no console errors, no broken images,
no horizontal page overflow, and the battle smoke test reached the dock.
Writes qa-out/report.json and one screenshot per screen; that JSON line
"QA RESULT: PASS|FAIL" is what a /goal condition can point at.

Requires: pip install playwright && playwright install chromium
WebGL runs on SwiftShader here, so frame times are NOT representative of a phone.
"""
import argparse, json, os, pathlib, sys, time
from playwright.sync_api import sync_playwright

VIEWPORTS = {
    'mobile': dict(viewport={'width': 390, 'height': 844}, has_touch=True, is_mobile=True, device_scale_factor=1),
    'tablet': dict(viewport={'width': 1024, 'height': 768}, has_touch=True, is_mobile=False, device_scale_factor=1),
    'desktop': dict(viewport={'width': 1440, 'height': 900}, device_scale_factor=1),
}
ROUTES = ['hq', 'arsenal', 'rewards', 'campaign', 'more']

LINT_JS = r"""
(({minTap}) => {
  const vis = el => { const r = el.getBoundingClientRect(); const cs = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; };
  const label = el => (el.id ? '#' + el.id : el.tagName.toLowerCase()) +
    (typeof el.className === 'string' && el.className ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '') +
    ' "' + (el.getAttribute('aria-label') || el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 40) + '"';
  const broken = [...document.images].filter(i => vis(i) && i.complete && i.naturalWidth === 0).map(label);
  const overflowX = document.documentElement.scrollWidth > innerWidth + 1;
  const clipped = [...document.querySelectorAll('button, .pill, h1, h2, h3')].filter(el => vis(el) &&
    getComputedStyle(el).overflow !== 'visible' && el.scrollWidth > el.clientWidth + 2).map(label).slice(0, 25);
  const small = minTap ? [...document.querySelectorAll('button, a, select, input')].filter(el => {
    if (!vis(el)) return false; const r = el.getBoundingClientRect();
    return (r.width < minTap || r.height < minTap) && r.top < innerHeight && r.bottom > 0; }).map(label).slice(0, 25) : [];
  const squeezed = [...document.querySelectorAll('#menu-content button, #menu-content section, #menu-content aside')]
    .filter(el => vis(el) && el.getBoundingClientRect().width < 60 && el.getBoundingClientRect().height > 80).map(label);
  const tiny = [...document.querySelectorAll('#menu-content *, #combat-dock *')].filter(el => el.childElementCount === 0 &&
    el.textContent.trim() && vis(el) && parseFloat(getComputedStyle(el).fontSize) < 10).map(label).slice(0, 25);
  return { broken, overflowX, clipped, smallTargets: small, squeezed, tinyText: tiny };
})
"""


def run(game, out, viewports, battle_seconds, do_menu=True, do_battle=True):
    os.makedirs(out, exist_ok=True)
    report = {'game': os.path.basename(game), 'viewports': {}, 'problems': []}
    with sync_playwright() as p:
        browser = p.chromium.launch(args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
        for vp in viewports:
            ctx = browser.new_context(**VIEWPORTS[vp])
            page = ctx.new_page()
            log = []
            page.on('console', lambda m: log.append(f'{m.type}: {m.text[:300]}') if m.type in ('error', 'warning') else None)
            page.on('pageerror', lambda e: log.append(f'PAGEERROR: {str(e)[:400]}'))
            r = {'screens': {}, 'console': log}
            t0 = time.time()
            page.goto(pathlib.Path(game).resolve().as_uri(), wait_until='load', timeout=180000)
            page.wait_for_function("document.getElementById('boot').hidden", timeout=90000)
            r['boot_s'] = round(time.time() - t0, 1)
            r['title'] = page.title()
            time.sleep(1.0)
            min_tap = 40 if vp == 'mobile' else 0
            for route in (ROUTES if do_menu else []):
                page.click(f'#menu-nav button[data-route="{route}"]')
                time.sleep(0.7)
                shots, k = [], 0
                h = page.evaluate("document.getElementById('menu-content').scrollHeight")
                ch = page.evaluate("document.getElementById('menu-content').clientHeight")
                while True:
                    name = f'{vp}_{route}_{k}.png'
                    page.screenshot(path=os.path.join(out, name)); shots.append(name)
                    k += 1
                    if k * ch * 0.9 >= h - ch or k >= 5:
                        break
                    page.evaluate(f"document.getElementById('menu-content').scrollTop={int(k * ch * 0.9)}"); time.sleep(0.35)
                page.evaluate("document.getElementById('menu-content').scrollTop=0"); time.sleep(0.2)
                lint = page.evaluate(LINT_JS, {'minTap': min_tap})
                r['screens'][route] = {'shots': shots, 'scroll_screens': k, **lint}
            if do_menu:
                page.click('#menu-settings'); time.sleep(0.6)
                page.screenshot(path=os.path.join(out, f'{vp}_settings.png'))
                # UX assertion: the launch button is fully visible on the first HQ screen
                page.click('#menu-nav button[data-route="hq"]'); time.sleep(0.6)
                r['launch_first_screen'] = page.evaluate("""(()=>{const b=document.getElementById('launch'),n=document.getElementById('menu-nav');
                  if(!b)return false;const r=b.getBoundingClientRect();return r.top>=0&&r.bottom<=n.getBoundingClientRect().top;})()""")
            # battle smoke test: quick battle from HQ
            page.click('#menu-nav button[data-route="hq"]'); time.sleep(0.6)
            battle = {'ok': True, 'skipped': True}
            if do_battle:
              battle = {'ok': False}
              try:
                  page.evaluate("document.querySelector('#launch').scrollIntoView({block:'center'})")
                  page.click('#launch'); time.sleep(3)
                  page.wait_for_selector('#combat-dock .slot-btn', timeout=60000)
                  page.screenshot(path=os.path.join(out, f'{vp}_battle_start.png'), timeout=180000)
                  ids_before = page.evaluate("[...document.querySelectorAll('#combat-dock .slot-btn')].map(b=>b.dataset.qa??=Math.random())")
                  time.sleep(1.5)
                  battle['dock_stable'] = page.evaluate("[...document.querySelectorAll('#combat-dock .slot-btn')].every(b=>b.dataset.qa)")
                  page.click('#combat-dock .slot-btn[data-pad="0"]'); time.sleep(0.8)
                  battle['build_cards'] = page.evaluate("document.querySelectorAll('.build-card').length")
                  page.screenshot(path=os.path.join(out, f'{vp}_battle_build.png'), timeout=180000)
                  if battle['build_cards']:
                      page.click('.build-card'); time.sleep(1.0)
                  time.sleep(battle_seconds)
                  battle['clock'] = page.inner_text('#clock')
                  battle['perf'] = page.evaluate("document.getElementById('perf').textContent")
                  page.screenshot(path=os.path.join(out, f'{vp}_battle_later.png'), timeout=180000)
                  page.click('#pause-button'); time.sleep(0.7)
                  page.screenshot(path=os.path.join(out, f'{vp}_battle_pause.png'), timeout=180000)
                  battle['lint'] = page.evaluate(LINT_JS, {'minTap': min_tap})
                  battle['ok'] = battle['build_cards'] > 0
              except Exception as e:  # noqa: BLE001 - report, don't crash the run
                  battle['error'] = str(e)[:300]
            r['battle'] = battle
            report['viewports'][vp] = r
            ctx.close()
        browser.close()
    # verdict
    for vp, r in report['viewports'].items():
        errs = [l for l in r['console'] if l.startswith(('error', 'PAGEERROR'))]
        if errs: report['problems'].append(f'{vp}: {len(errs)} console/page errors')
        for route, sc in r['screens'].items():
            if sc['broken']: report['problems'].append(f'{vp}/{route}: broken images {sc["broken"]}')
            if sc['overflowX']: report['problems'].append(f'{vp}/{route}: horizontal page overflow')
            if sc['squeezed']: report['problems'].append(f'{vp}/{route}: squeezed blocks {sc["squeezed"]}')
        if r.get('launch_first_screen') is False: report['problems'].append(f'{vp}: launch button not on the first HQ screen')
        if not r['battle'].get('ok'): report['problems'].append(f'{vp}: battle smoke failed {r["battle"].get("error", "")}')
    report['result'] = 'PASS' if not report['problems'] else 'FAIL'
    json.dump(report, open(os.path.join(out, 'report.json'), 'w'), ensure_ascii=False, indent=1)
    for vp, r in report['viewports'].items():
        print(f"[{vp}] boot {r['boot_s']}s · title «{r['title']}» · battle {r['battle']}")
        for route, sc in r['screens'].items():
            print(f"   {route:9s} screens={sc['scroll_screens']} small_targets={len(sc['smallTargets'])} clipped={len(sc['clipped'])} tiny_text={len(sc['tinyText'])}")
        if 'launch_first_screen' in r: print(f"   launch button on first HQ screen: {r['launch_first_screen']}")
    for pr in report['problems']:
        print(' !', pr)
    print(f"QA RESULT: {report['result']}")
    return 0 if report['result'] == 'PASS' else 1


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('game')
    ap.add_argument('--out', default='qa-out')
    ap.add_argument('--viewports', default='mobile,desktop')
    ap.add_argument('--battle-seconds', type=int, default=15)
    ap.add_argument('--no-battle', action='store_true', help='menu tour only')
    ap.add_argument('--battle-only', action='store_true', help='skip the menu tour')
    a = ap.parse_args()
    sys.exit(run(a.game, a.out, a.viewports.split(','), a.battle_seconds, not a.battle_only, not a.no_battle))
