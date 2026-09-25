#!/usr/bin/env python3
"""Measure the CPU cost of a dense battle, the part that does not depend on the GPU.

    python3 qa/perf.py GAME.html [--size army] [--difficulty normal] [--ticks 3600]

The 1.0.0 gate asks for 30+ FPS on a phone in a 220-point battle. Frame rate needs a
real device - this container renders on SwiftShader - but the work the CPU does every
tick does not: simulation step cost and pose building are the same code on any device,
and they set the ceiling the GPU then has to fit under.

Reports milliseconds per simulated tick at the point the field is busiest.

This is a REGRESSION gauge, not an absolute verdict. The container CPU is not a phone
CPU, so the millisecond figure means nothing on its own; what means something is the
same number measured on two builds. Run it, compare against qa/perf-baseline.json, and
treat a jump as a regression to explain. The 30 FPS clause of the 1.0.0 gate still needs
a real device - see docs/ROADMAP.md.

Pose time in the report is inflated by design: the harness steps hundreds of ticks
between draws, so every draw rebuilds a cold pose cache. Read sim ms/tick, not poseMs.
"""
import argparse, json, pathlib, sys, time
from playwright.sync_api import sync_playwright

SETUP = """([size,difficulty])=>{
  const s=TerraDebug; s.showMenu('hq');
  const settings=globalThis.TERRA_SETTINGS||null;
  return {size,difficulty};
}"""
MEASURE = """(n)=>{
  const t0=performance.now();
  TerraDebug.step(n);
  const dt=performance.now()-t0;
  const s=TerraDebug.state, m=TerraDebug.metrics;
  return {msPerTick:dt/n, ticks:s.tick, units:s.units.length,
          structures:s.structures.filter(p=>p.hp>0).length,
          population:[s.teams[0].deck?1:0],
          parts:m.parts, actors:m.actors, drawCalls:m.drawCalls, triangles:m.triangles,
          poseMs:m.poseMs, submitMs:m.submitMs};
}"""
BUILD = """(()=>{
  const s=TerraDebug.state, team=s.teams[0];
  const spawners=(globalThis.TERRA_BALANCE.spawners||[]).filter(b=>(b.kind||'spawner')==='spawner').map(b=>b.id);
  const pick=team.deck.filter(id=>spawners.includes(id));
  if(!pick.length)return {built:0};
  let built=0;
  for(let lane=0;lane<3;lane++)for(let pad=0;pad<3;pad++){
    const bp=pick[(lane+pad)%pick.length];
    const ack=TerraDebug.command({type:'build',lane,pad,blueprint:bp});
    if(ack&&ack.ok)built++;
  }
  return {built};
})()"""


def run(game, size, difficulty, ticks):
    with sync_playwright() as pw:
        b = pw.chromium.launch(args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
        ctx = b.new_context(viewport={'width': 390, 'height': 844}, has_touch=True, is_mobile=True)
        page = ctx.new_page(); errors = []
        page.on('pageerror', lambda e: errors.append(str(e)[:200]))
        page.goto(pathlib.Path(game).resolve().as_uri() + '?test=1', wait_until='load', timeout=180000)
        page.wait_for_function("document.getElementById('boot').hidden", timeout=120000)
        time.sleep(1.0)
        page.evaluate("window.__TERRA_MANUAL_FRAME__=true")
        page.click(f'#menu-nav button[data-route="hq"]'); time.sleep(0.5)
        # Size and difficulty live inside a collapsed <details>. Clicks are delegated on
        # document, so dispatching them drives exactly the handler a tap would.
        picked = page.evaluate("""([size,difficulty])=>{
          const s=document.querySelector(`[data-battle-size="${size}"]`);
          const d=document.querySelector(`[data-difficulty="${difficulty}"]`);
          if(s)s.click(); if(d)d.click();
          return {size:!!s, difficulty:!!d};
        }""", [size, difficulty])
        if not (picked['size'] and picked['difficulty']):
            raise SystemExit(f'controls not found: {picked}')
        time.sleep(0.6)
        page.evaluate("TerraDebug.start(null)"); time.sleep(1.5)
        built = page.evaluate(BUILD)
        samples, chunk = [], 300
        done = 0
        while done < ticks:
            row = page.evaluate(MEASURE, chunk)
            page.evaluate(BUILD)          # keep the field populated
            samples.append(row)
            done += chunk
            if row['ticks'] >= 20 * 60 * 10:
                break
        peak = max(samples, key=lambda r: r['units'])
        busy = [r for r in samples if r['units'] >= peak['units'] * 0.6] or samples
        mean = sum(r['msPerTick'] for r in busy) / len(busy)
        baseline_path = pathlib.Path(__file__).with_name('perf-baseline.json')
        baseline = json.loads(baseline_path.read_text()) if baseline_path.exists() else None
        verdict, note = 'PASS', 'no baseline stored yet'
        if errors:
            verdict, note = 'FAIL', f'{len(errors)} page errors'
        elif baseline:
            ref = baseline.get('mean_ms_per_tick_busy')
            if ref:
                delta = (mean - ref) / ref * 100
                note = f'{mean:.2f} vs baseline {ref:.2f} ms/tick ({delta:+.0f}%)'
                if delta > 15:
                    verdict = 'FAIL'
        out = {'game': pathlib.Path(game).name, 'size': size, 'difficulty': difficulty,
               'built': built.get('built'), 'samples': samples, 'peak': peak, 'errors': errors,
               'mean_ms_per_tick_busy': round(mean, 3), 'peak_units': peak['units'],
               'comparison': note, 'result': verdict}
        json.dump(out, open('perf-report.json', 'w'), ensure_ascii=False, indent=1)
        for r in samples:
            print(f"  tick {r['ticks']:5d} units {r['units']:3d} parts {r['parts']:4d} "
                  f"sim {r['msPerTick']:5.2f} ms/tick  pose {r['poseMs']:5.2f} ms")
        print(f"peak {peak['units']} units · busy mean {mean:.2f} ms/tick · {note}")
        if errors:
            print(' ! page errors:', errors[:2])
        print(f"PERF RESULT: {out['result']}")
        ctx.close(); b.close()
        return 0 if out['result'] == 'PASS' else 1


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('game'); ap.add_argument('--size', default='army')
    ap.add_argument('--difficulty', default='normal'); ap.add_argument('--ticks', type=int, default=3600)
    a = ap.parse_args()
    sys.exit(run(a.game, a.size, a.difficulty, a.ticks))
