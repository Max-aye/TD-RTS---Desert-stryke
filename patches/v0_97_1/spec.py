"""TERRA 2136 v0.97.1 — model textures fit the device, bodies bank into turns.

Anchors come from v0.97.0 and must match exactly. Render-only: nothing is written
to sim.s, no Math.random or Date.now feeds gameplay, balance and the save format
are untouched.
"""
VERSION = '0.97.1'

ROOT = """function rootInto(o,x,y,z,s,heading,lean=0,roll=0){/* MODELS-0971 */
 const c=Math.cos(heading),a=Math.sin(heading),cl=Math.cos(lean),sl=Math.sin(lean);
 let X0=c,X1=0,X2=-a,Y0=a*sl,Y1=cl,Y2=c*sl;const Z0=a*cl,Z1=-sl,Z2=c*cl;
 /* Roll turns the body around its own forward axis, so pitch and heading survive it. */
 if(roll){const cr=Math.cos(roll),sr=Math.sin(roll);
  const nx0=X0*cr+Y0*sr,nx1=X1*cr+Y1*sr,nx2=X2*cr+Y2*sr;
  Y0=Y0*cr-X0*sr;Y1=Y1*cr-X1*sr;Y2=Y2*cr-X2*sr;X0=nx0;X1=nx1;X2=nx2;}
 o[0]=X0*s;o[1]=X1*s;o[2]=X2*s;o[3]=0;o[4]=Y0*s;o[5]=Y1*s;o[6]=Y2*s;o[7]=0;
 o[8]=Z0*s;o[9]=Z1*s;o[10]=Z2*s;o[11]=0;o[12]=x;o[13]=y;o[14]=z;o[15]=1;return o;"""

TEXTURE = """const cap0971=this.textureCap0971||2048;let source0971=image;
    /* MODELS-0971: embedded GLB textures were uploaded at source size on every device.
     * Downscaling to the quality cap cuts GPU texture memory without touching the asset. */
    if(Math.max(image.width,image.height)>cap0971){
     const k=cap0971/Math.max(image.width,image.height),canvas=document.createElement('canvas');
     canvas.width=Math.max(1,Math.round(image.width*k));canvas.height=Math.max(1,Math.round(image.height*k));
     const cx=canvas.getContext('2d');
     if(cx){cx.imageSmoothingEnabled=true;cx.imageSmoothingQuality='high';cx.drawImage(image,0,0,canvas.width,canvas.height);source0971=canvas;}
    }
    const t=g.createTexture();textures.set(im.key,t);g.bindTexture(g.TEXTURE_2D,t);g.pixelStorei(g.UNPACK_FLIP_Y_WEBGL,false);g.texImage2D(g.TEXTURE_2D,0,g.RGBA,g.RGBA,g.UNSIGNED_BYTE,source0971);"""

BANK = """  /* MODELS-0971: bank into the turn. Heading rate is measured from the render actor's
   * own previous heading, so nothing is read back from or written to the simulation. */
  const previousHeading=actor.heading0971;actor.heading0971=u.heading;
  let turn=previousHeading===undefined?0:u.heading-previousHeading;
  while(turn>Math.PI)turn-=Math.PI*2;while(turn<-Math.PI)turn+=Math.PI*2;
  const rate=step?turn/step:0;
  const bank=clamp(rate*Math.min(1,actor.speed097/3.2)*.22,.17);
  const roll=actor.roll0971??0;
  actor.roll0971=step?roll+(bank-roll)*(1-Math.exp(-step/.13)):bank;
  return actor.lean097;/* MODELS-0971 */
 }"""

EDITS = [
 dict(file='markup/head.html', old='<title>TERRA 2136 · v0.97.0</title>',
      new='<title>TERRA 2136 · v{{VERSION}}</title>', why='tab title still on 0.97.0'),
 dict(file='markup/body.html', old='<small>Офлайн-версия 0.97.0</small>',
      new='<small>Офлайн-версия {{VERSION}}</small>', why='boot screen still on 0.97.0'),
 dict(file='markup/body.html', old='<div class="build-stamp">TERRA 2136 · 0.97.0 · офлайн</div>',
      new='<div class="build-stamp">TERRA 2136 · {{VERSION}} · офлайн</div>', why='menu stamp still on 0.97.0'),
 dict(file='ui/version95.js', old="globalThis.TERRA_VERSION='0.97.0';",
      new="globalThis.TERRA_VERSION='{{VERSION}}';", why='single source of truth for the build number'),

 # --- model textures sized for the device -----------------------------------------------
 dict(file='render/adapters.js',
      old="const t=g.createTexture();textures.set(im.key,t);g.bindTexture(g.TEXTURE_2D,t);g.pixelStorei(g.UNPACK_FLIP_Y_WEBGL,false);g.texImage2D(g.TEXTURE_2D,0,g.RGBA,g.RGBA,g.UNSIGNED_BYTE,image);",
      new=TEXTURE, why='23 MB of model textures uploaded at source size even on a phone'),
 dict(file='render/adapters.js',
      old='out.textureBytes+=Math.ceil(image.width*image.height*4*4/3);return t;',
      new='out.textureBytes+=Math.ceil(source0971.width*source0971.height*4*4/3);return t;/* MODELS-0971 */',
      why='texture budget must count what was actually uploaded'),
 dict(file='render/adapters.js',
      old='prewarm(s,settings=this.assetSettings){this.assetSettings=settings;',
      new="prewarm(s,settings=this.assetSettings){/* MODELS-0971 */this.assetSettings=settings;"
          "this.imported.textureCap0971=this.r.quality==='low'?512:this.r.quality==='high'?2048:1024;",
      why='the cap must be known before the first model upload'),

 # --- bank into turns --------------------------------------------------------------------
 dict(file='render/adapters.js',
      old="function rootInto(o,x,y,z,s,heading,lean=0){const c=Math.cos(heading),a=Math.sin(heading),cl=Math.cos(lean),sl=Math.sin(lean);o[0]=c*s;o[1]=0;o[2]=-a*s;o[3]=0;o[4]=a*sl*s;o[5]=cl*s;o[6]=c*sl*s;o[7]=0;o[8]=a*cl*s;o[9]=-sl*s;o[10]=c*cl*s;o[11]=0;o[12]=x;o[13]=y;o[14]=z;o[15]=1;return o;",
      new=ROOT, why='the transform had no roll channel at all'),
 dict(file='render/adapters.js',
      old='update(sample,x,y,z,scale,heading,hit=0,lean=0,dt=1/60){const {a,b,mix}=sample;rootInto(this.root,x,y,z,scale,heading,lean);',
      new='update(sample,x,y,z,scale,heading,hit=0,lean=0,dt=1/60,roll=0){const {a,b,mix}=sample;rootInto(this.root,x,y,z,scale,heading,lean,roll);/* MODELS-0971 */',
      why='actors could not carry a roll angle'),
 dict(file='render/adapters.js', old='  return actor.lean097;\n }', new=BANK,
      why='heading rate drives the bank, smoothed on the render actor'),
 dict(file='render/adapters.js',
      old='hit*.085+this.actorLean097(actor,u,x,z,s.paused?0:renderDt),s.paused?0:renderDt);/* MODELS-097 */',
      new='hit*.085+this.actorLean097(actor,u,x,z,s.paused?0:renderDt),s.paused?0:renderDt,actor.roll0971||0);/* MODELS-0971 */',
      why='pass the banked roll to the actor transform'),
]
