"""TERRA 2136 v0.99.1 — R2: политика терминала V2 с миграцией истории.

Anchors come from v0.99.0 and must match exactly.

Разбор наград (R2) предлагал убрать пустой исход терминала, но относил это к правкам
«только данные и формулы». Это не так: валидатор журнала пересчитывает каждую квитанцию
и сверяет точные выплаты, поэтому смена выплаты задним числом сделала бы ранее записанные
квитанции невалидными и сломала бы сохранение. Здесь сделано по-настоящему: версия
политики плюс миграция.

Что НЕ меняется: веса исходов, пулы карт, гарантия (pityAt=8) и поток ГПСЧ. Любая
ранее записанная квитанция пересчитывается в точности как раньше.

Что меняется: исход «empty» теперь приносит одну деталь модуля — но только начиная
с того прокрута, на котором профиль перешёл на V2. `terminal.v2From` хранит последний
номер, оплаченный по старой таблице, поэтому вся прежняя история остаётся валидной.
Номер политики не пишется в саму квитанцию: набор её полей проверяется на точное
совпадение, и лишнее поле сломало бы старые записи.
"""
VERSION = '0.99.1'

POLICY = """/* TERMINAL-V2 (R2): «Без награды» выпадала в 40% прокрутов и не давала ничего.
 * Бросок не тронут — те же веса, пулы, гарантия и поток ГПСЧ, поэтому любая ранее
 * записанная квитанция пересчитывается в точности как раньше. Меняется только выплата,
 * и только с того прокрута, на котором профиль перешёл на V2. */
const TERMINAL_PAYOUT={
 1:{parts:{modParts:3},shards:{techShards:3}},
 2:{parts:{modParts:3},shards:{techShards:3},empty:{modParts:1}}
};
function terminalPayout(sequence,v2From,outcome){
 const row=TERMINAL_PAYOUT[sequence>v2From?2:1][outcome]||{};
 return {modParts:row.modParts||0,techShards:row.techShards||0};
}
function terminalDefaults(seed){return {version:2,rng:((seed>>>0)^TERMINAL_V1.salt)>>>0,pity:0,seq:0,v2From:0,history:[]};}"""

MIGRATE = """ /* TERMINAL-V2: сохранение версии 1 переводится на версию 2 здесь. Все его квитанции
  * остаются оплаченными по старой таблице (v2From = seq), новый прокрут идёт по новой. */
 if(keys(input,['version','rng','pity','seq','history'])&&input.version===1)input={...input,version:2,v2From:input.seq};
 if(!keys(input,['version','rng','pity','seq','v2From','history'])||input.version!==2||!integer(input.v2From)||input.v2From>input.seq||"""

EDITS = [
 dict(file='markup/head.html', old='<title>TERRA 2136 · v0.99.0</title>',
      new='<title>TERRA 2136 · v{{VERSION}}</title>', why='tab title still on 0.99.0'),
 dict(file='markup/body.html', old='<small>Офлайн-версия 0.99.0</small>',
      new='<small>Офлайн-версия {{VERSION}}</small>', why='boot screen still on 0.99.0'),
 dict(file='markup/body.html', old='<div class="build-stamp">TERRA 2136 · 0.99.0 · офлайн</div>',
      new='<div class="build-stamp">TERRA 2136 · {{VERSION}} · офлайн</div>', why='menu stamp still on 0.99.0'),
 dict(file='ui/version95.js', old="globalThis.TERRA_VERSION='0.99.0';",
      new="globalThis.TERRA_VERSION='{{VERSION}}';", why='single source of truth for the build number'),

 dict(file='game/progress.js',
      old="function terminalDefaults(seed){return {version:1,rng:((seed>>>0)^TERMINAL_V1.salt)>>>0,pity:0,seq:0,history:[]};}",
      new=POLICY, why='payout tables per policy version; fresh profiles start on V2'),
 dict(file='game/progress.js',
      old="if(!keys(input,['version','rng','pity','seq','history'])||input.version!==1||",
      new=MIGRATE, why='accept a V1 journal and migrate it, then validate the V2 shape'),
 dict(file='game/progress.js',
      old="if(r.modParts!==(r.outcome==='parts'?3:0)||r.techShards!==(r.outcome==='shards'?3:0))fail();",
      new="const pay=terminalPayout(r.sequence,input.v2From,r.outcome);/* TERMINAL-V2 */\n"
          "  if(r.modParts!==pay.modParts||r.techShards!==pay.techShards)fail();",
      why='each receipt is checked against the table that paid it'),
 dict(file='game/progress.js',
      old="card:null,modParts:roll.outcome==='parts'?3:0,techShards:roll.outcome==='shards'?3:0};",
      new="card:null,...terminalPayout(t.seq+1,t.v2From,roll.outcome)};/* TERMINAL-V2 */",
      why='a new spin is paid by the policy in force for its sequence'),

 # --- тексты интерфейса: исход больше не пустой ------------------------------------------
 dict(file='data/design-config.js', old='"label": "Без награды"', new='"label": "Малый пакет"',
      why='the outcome now returns a module part'),
 dict(file='ui/views.js',
      old="const labels={empty:'Без награды',parts:'Детали модулей',shards:'Осколки технологий',rare:'Редкая карта',epic:'Эпическая карта',legendary:'Легендарная карта'};",
      new="const labels={empty:'Малый пакет',parts:'Детали модулей',shards:'Осколки технологий',rare:'Редкая карта',epic:'Эпическая карта',legendary:'Легендарная карта'};/* TERMINAL-V2 */",
      why='odds panel called the outcome empty'),
 dict(file='ui/views.js',
      old="'Без награды: 40%. После 7 попыток без карты следующая даст редкую или лучше.'",
      new="'Малый пакет: 40% — одна деталь модуля. После 7 попыток без карты следующая даст редкую или лучше.'",
      why='odds text described the old empty outcome'),
 dict(file='ui/views.js',
      old="r.outcome==='empty'?`<div class=\"reward-symbol\">${I('close')}</div><h3>Без награды</h3>`",
      new="r.outcome==='empty'?`<div class=\"reward-symbol\">${I(r.modParts>0?'gear':'close')}</div>"
          "<h3>${r.modParts>0?'Малый пакет':'Без награды'}</h3>"
          "${r.modParts>0?`<p>+${r.modParts} деталь модуля</p>`:''}`",
      why='the result screen must show what the receipt actually paid, old and new alike'),
]
