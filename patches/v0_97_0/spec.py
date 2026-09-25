"""TERRA 2136 v0.97.0 — unit models: detail, textures, motion, budget.

Anchors come from v0.96.0 and must match exactly. Everything here is render-only:
no simulation state is written, no Math.random or Date.now feeds gameplay, and
balance and the save format are untouched.
"""
VERSION = '0.97.0'

# --- render-only lean: acceleration pitch plus ground slope, spring-smoothed ----------------
LEAN = """ /* MODELS-097: render-only body pitch. Reads interpolated render position and the
  * height field, keeps its state on the render actor, and never writes to sim.s.
  * The existing `lean` channel of TerraPose.Actor is a pitch around the model's side axis:
  * a positive value noses the model down. */
 actorLean097(actor,u,x,z,dt){
  const step=Math.max(0,Math.min(.05,dt));
  const speed=Math.hypot(u.x-u.previousX,u.z-u.previousZ)*20;
  const previous=actor.speed097??speed;
  actor.speed097=previous+(speed-previous)*(step?1-Math.exp(-step/.05):1);
  const accel=step?(actor.speed097-previous)/step:0;
  const ahead=Math.sin(u.heading)*.85,side=Math.cos(u.heading)*.85;
  const slope=(this.surface(x+ahead,z+side)-this.surface(x-ahead,z-side))/1.7;
  const clamp=(v,limit)=>Math.max(-limit,Math.min(limit,v));
  const target=clamp(-accel*.045,.12)+clamp(-slope*.6,.16);
  const lean=actor.lean097??0;
  actor.lean097=step?lean+(target-lean)*(1-Math.exp(-step/.11)):target;
  return actor.lean097;
 }
 /* MODELS-097: one detail decision per frame for the whole field. detailScale097 is
  * pixels per metre of the real drawing buffer, so it already accounts for device
  * resolution, zoom and the adaptive render scale. */
 frame097(){
  this.detailScale097=this.canvas.clientHeight/Math.max(.001,this.r.span)*(this.r.renderScale||1);
  this.detailBudget097=this.r.quality==='high'?24:12;
 }
"""

# --- detail chosen by on-screen size, with a per-frame budget -------------------------------
DETAIL = """   /* MODELS-097: the camera is orthographic, so on-screen size is model size x pixels
    * per metre - raw zoom ignored device resolution and the adaptive render scale.
    * Measured: 2.4-3.5 px/m on a 390 px phone at zoom 1, 9.2 on desktop; 11% hysteresis
    * stops the mesh swapping on small zoom changes; the budget keeps
    * a crowded field from paying for detail meshes it cannot show anyway. */
   const detailPx=SCALE[renderKind]*this.detailScale097;
   const wasDetail=actor.detail097===true;
   const detail=this.r.quality!=='low'&&this.detailBudget097>0&&detailPx>=(wasDetail?5.8:6.5);
   actor.detail097=detail;if(detail&&!wasDetail)this.detailBudget097--;
   const assetId=root.TerraImported.choice(s,u,this.assetSettings);"""

FRAME = """  const items=this.items;items.length=0;this.liveIds.clear();const marks=new Model();this.frame097();let actors=0;"""

EDITS = [
 # --- one version number ---------------------------------------------------------------
 dict(file='markup/head.html', old='<title>TERRA 2136 · v0.96.0</title>',
      new='<title>TERRA 2136 · v{{VERSION}}</title>', why='tab title still on 0.96.0'),
 dict(file='markup/body.html', old='<small>Офлайн-версия 0.96.0</small>',
      new='<small>Офлайн-версия {{VERSION}}</small>', why='boot screen still on 0.96.0'),
 dict(file='markup/body.html', old='<div class="build-stamp">TERRA 2136 · 0.96.0 · офлайн</div>',
      new='<div class="build-stamp">TERRA 2136 · {{VERSION}} · офлайн</div>', why='menu stamp still on 0.96.0'),
 dict(file='ui/version95.js', old="globalThis.TERRA_VERSION='0.96.0';",
      new="globalThis.TERRA_VERSION='{{VERSION}}';", why='single source of truth for the build number'),

 # --- textures: the anisotropy ceiling was 4 even where the GPU offers 16 ----------------
 dict(file='render/adapters.js',
      old='this.maxAnisotropy=this.anisotropy?Math.min(4,g.getParameter(this.anisotropy.MAX_TEXTURE_MAX_ANISOTROPY_EXT)):1;',
      new='this.maxAnisotropy=this.anisotropy?Math.min(8,g.getParameter(this.anisotropy.MAX_TEXTURE_MAX_ANISOTROPY_EXT)):1;/* MODELS-097 */',
      why='imported model textures were capped at 4x anisotropy'),
 dict(file='render/adapters.js',
      old="anisotropy=Math.min(this.maxAnisotropy,options.quality==='low'?1:options.quality==='medium'?2:4)",
      new="anisotropy=Math.min(this.maxAnisotropy,options.quality==='low'?1:options.quality==='medium'?4:8)/* MODELS-097 */",
      why='grazing-angle blur on unit and building surfaces at medium and high quality'),
 dict(file='engine/ark-visual-a.js',
      old="Math.min(this.quality === 'high' ? 4 : 2, this.maxAnisotropy)",
      new="Math.min(this.quality === 'high' ? 8 : 4, this.maxAnisotropy) /* MODELS-097 */",
      why='material texture array had the same 4x/2x ceiling'),

 # --- detail by on-screen size, bounded by a per-frame budget ---------------------------
 dict(file='render/adapters.js',
      old="   const detail=this.r.quality!=='low'&&(this.zoom>=1.22||this.r.quality==='high');const assetId=root.TerraImported.choice(s,u,this.assetSettings);",
      new=DETAIL,
      why='detail meshes never appeared on a phone at default zoom, and were unbounded when they did'),

 # --- render-only body pitch on the procedural units ------------------------------------
 dict(file='render/adapters.js',
      old='actor.update(sample,x,groundY+.018,z,SCALE[renderKind],u.heading,hit,hit*.085,s.paused?0:renderDt);',
      new='actor.update(sample,x,groundY+.018,z,SCALE[renderKind],u.heading,hit,'
          'hit*.085+this.actorLean097(actor,u,x,z,s.paused?0:renderDt),s.paused?0:renderDt);/* MODELS-097 */',
      why='units kept a rigid vertical body while accelerating, braking and crossing slopes'),
 dict(file='render/adapters.js',
      old='  const items=this.items;items.length=0;this.liveIds.clear();const marks=new Model();let actors=0;',
      new=FRAME, why='per-frame detail scale and budget for the actor loop'),
 dict(file='render/adapters.js', old=' metrics(){return {...this.perf,',
      new=LEAN + ' metrics(){/* MODELS-097 */return {...this.perf,detailScale097:+(this.detailScale097||0).toFixed(1),'
          'detailActors097:[...this.actors.values()].filter(a=>a.detail097).length,',
      why='lean helper on the Battlefield class; detail counters for QA'),
]
