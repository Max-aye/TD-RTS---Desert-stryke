"""TERRA 2136 v0.98.0 — rewards R1 and R4 (balance task, see docs/CHANGELOG.md).

Anchors come from v0.97.1 and must match exactly. This version changes reward
numbers, so it carries a "было → стало" table in the changelog, as the project
rules require. The simulation and the save format are untouched: the only new
stored field is an optional daily counter that normalize() merges over defaults,
so a save written before this version loads unchanged with the counter at 0.

R2 (terminal consolation) and R3 (calendar curve) are deliberately NOT here;
docs/REWARDS_REVIEW.md records why.
"""
VERSION = '0.98.0'

REPEAT = """/* REWARDS-098 (R1): a repeat used to pay a flat table value - 40 alloy against the
 * 180 of the first clear on M01, or 22%. It now pays REPEAT_SHARE_098 of the first
 * clear for the first REPEAT_CAP_098 repeats of a day, and the old table value after
 * that, so replaying is worth it without becoming a farm. The counter lives on
 * missionsDaily, which normalize() merges over defaults: older saves load with 0. */
const REPEAT_SHARE_098=.35,REPEAT_CAP_098=5;
function repeatReward098(m,mission){
 const day=m.missionsDaily,used=day.repeats||0;
 const out=copy(mission.repeat);
 if(used>=REPEAT_CAP_098)return out;
 day.repeats=used+1;
 for(const k of ['alloy','polymer','intel']){
  const full=mission.reward[k];
  if(full)out[k]=Math.max(out[k]||0,Math.round(full*REPEAT_SHARE_098));
 }
 return out;
}
function refreshDay(m,now/* REWARDS-098 */){"""

EDITS = [
 dict(file='markup/head.html', old='<title>TERRA 2136 · v0.97.1</title>',
      new='<title>TERRA 2136 · v{{VERSION}}</title>', why='tab title still on 0.97.1'),
 dict(file='markup/body.html', old='<small>Офлайн-версия 0.97.1</small>',
      new='<small>Офлайн-версия {{VERSION}}</small>', why='boot screen still on 0.97.1'),
 dict(file='markup/body.html', old='<div class="build-stamp">TERRA 2136 · 0.97.1 · офлайн</div>',
      new='<div class="build-stamp">TERRA 2136 · {{VERSION}} · офлайн</div>', why='menu stamp still on 0.97.1'),
 dict(file='ui/version95.js', old="globalThis.TERRA_VERSION='0.97.1';",
      new="globalThis.TERRA_VERSION='{{VERSION}}';", why='single source of truth for the build number'),

 # --- R1: a repeat is worth 35% of the first clear, five a day ---------------------------
 dict(file='game/progress.js', old='function refreshDay(m,now){', new=REPEAT,
      why='repeat rewards were a flat table value worth ~22% of the first clear'),
 dict(file='game/progress.js',
      old="missionsDaily:{date:'',battles:0,kills:0,upgrades:0,claimed:[]}",
      new="missionsDaily:{date:'',battles:0,kills:0,upgrades:0,repeats:0,claimed:[]}",
      why='daily repeat counter, defaulted for saves written before this version'),
 dict(file='game/progress.js',
      old='m.missionsDaily={date:key,battles:0,kills:0,upgrades:0,claimed:[]};',
      new='m.missionsDaily={date:key,battles:0,kills:0,upgrades:0,repeats:0,claimed:[]};',
      why='the repeat counter resets with the rest of the daily counters'),
 dict(file='game/progress.js', old='Object.assign(r,firstWin?mission.reward:mission.repeat);',
      new='Object.assign(r,firstWin?mission.reward:repeatReward098(m,mission));/* REWARDS-098 */',
      why='route repeat wins through the R1 formula'),

 # --- R4: field loot is a real source ----------------------------------------------------
 dict(file='data/design-config.js',
      old='{"id":"alloy","name":"Сплав","icon":"cube","weight":45,"min":3,"max":7}',
      new='{"id":"alloy","name":"Сплав","icon":"cube","weight":45,"min":6,"max":12}',
      why='R4: a field find paid 3-7 alloy, below a single daily gift'),
]
