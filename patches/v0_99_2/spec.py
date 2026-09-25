"""TERRA 2136 v0.99.2 — экран запуска и загрузки.

Anchors come from v0.99.1. Presentation only: ни симуляция, ни баланс, ни формат
сохранений не затронуты, правок в контроллере нет.

Загрузка 43-мегабайтного файла на телефоне занимает заметное время, и всё это время
игрок видел статичную надпись. Теперь у запуска есть атмосфера и, что важнее, честная
обратная связь: полоса привязана к настоящим вехам (исполнение модулей, подготовка
WebGL и моделей, снятие экрана), а не к таймеру. Между вехами она движется с
затуханием и до края доходит только по реальному событию.

Вся графика — CSS и уже встроенный SVG: ни одной внешней загрузки, ни одного нового
растрового файла. Движение полностью отключается при prefers-reduced-motion.
"""
VERSION = '0.99.2'

EDITS = [
 dict(file='markup/head.html', old='<title>TERRA 2136 · v0.99.1</title>',
      new='<title>TERRA 2136 · v{{VERSION}}</title>', why='tab title still on 0.99.1'),
 dict(file='markup/body.html', old='<small>Офлайн-версия 0.99.1</small>',
      new='<small>Офлайн-версия {{VERSION}}</small>', why='boot screen still on 0.99.1'),
 dict(file='markup/body.html', old='<div class="build-stamp">TERRA 2136 · 0.99.1 · офлайн</div>',
      new='<div class="build-stamp">TERRA 2136 · {{VERSION}} · офлайн</div>', why='menu stamp still on 0.99.1'),
 dict(file='ui/version95.js', old="globalThis.TERRA_VERSION='0.99.1';",
      new="globalThis.TERRA_VERSION='{{VERSION}}';", why='single source of truth for the build number'),
 dict(file='markup/body.html',
      old='<p id="boot-message">Инициализация автономного прототипа…</p>',
      new='<p id="boot-message">Поднимаем связь с колониальным корпусом…</p>',
      why='the first line the player reads was developer wording'),
 dict(file='ui/controller.js',
      old="$('#boot-message').textContent='Подготовка WebGL, материалов и моделей…';",
      new="$('#boot-message').textContent='Собираем технику, броню и материалы…';/* BOOT-0992 */",
      why='the player was shown developer wording (WebGL) on the loading screen'),
]

NEW_PARTS = [
 dict(file='css/12-boot0992.css', source='boot0992.css', after='css/11-extra.css',
      glue_before='</style><style>'),
 dict(file='ui/boot0992.js', source='boot0992.js', after='ui/icons95.js',
      glue_before='</script><script>'),
]
