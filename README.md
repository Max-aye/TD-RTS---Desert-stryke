<div align="center">

# TERRA 2136 · Desert Stryke

<p align="center">
  <img src="./docs/before-after-mobile.png" alt="TERRA 2136 — Desert Stryke" width="900" />
</p>

<p align="center">
  <img alt="Status" src="https://img.shields.io/badge/status-active%20development-0.95.0-0A8F7A?style=for-the-badge" />
  <img alt="Platform" src="https://img.shields.io/badge/platform-browser%20%2F%20offline-FFB703?style=for-the-badge" />
  <img alt="Engine" src="https://img.shields.io/badge/render-WebGL2-1E90FF?style=for-the-badge" />
  <img alt="License" src="https://img.shields.io/badge/license-project%20internal-9B59B6?style=for-the-badge" />
</p>

### Офлайн tower offense / RTS в одном HTML-файле

Мобильная стратегия в стилистике марсианского фронта: стройте оборону, держите линию, запускайте отряды и выживайте в пустынной катастрофе — без сети, установки и лишних зависимостей.

<p align="center">
  <a href="./index.html"><img src="https://img.shields.io/badge/▶%20Запустить%20игру-FFD166?style=for-the-badge&logo=play&logoColor=101828" /></a>
  <a href="./TERRA2136_PLAY_v0.95.0.html"><img src="https://img.shields.io/badge/⬇%20Сборка-v0.95.0-7AE582?style=for-the-badge" /></a>
  <a href="./docs/ROADMAP.md"><img src="https://img.shields.io/badge/🗺%20Дорожная%20карта-9AA0FF?style=for-the-badge" /></a>
</p>

</div>

---

## Что это за проект

TERRA 2136 — это автономная браузерная стратегия с сильным визуальным характером и офлайн-выигрышной логикой. Игра собрана в одном HTML-файле, где сочетаются:

- тактический бой в реальном времени;
- кампания и карта-коллекция;
- система модулей, наград и прогресса;
- мобильный UI, адаптация под десктоп и телефон;
- WebGL2-рендер и встроенные ассеты без внешних загрузок.

> В текущем состоянии проект находится на версии `0.95.0` — это этап выравнивания структуры, иконок, порядков UX, читабельности интерфейса и стабильной QA-сборки.

---

## Особенности мира

| Элемент | Описание |
|---|---|
| Небо и стилистика | Марсианская пустыня, холодные оттенки, циан-металл и золотая бо́льшая палитра |
| Геймплей | Tower offense + RTS-логика управления линией фронта |
| Запуск | Офлайн, локально в браузере, без сетевых запросов |
| Инфраструктура | Один HTML-файл, собранный из `parts/` |
| Мобильность | Адаптирован под 390px, 1024px и desktop-разрешения |

---

## Быстрый старт

### Играть сразу

1. Откройте [`index.html`](./index.html)
2. Нажмите кнопку запуска
3. Или откройте готовую сборку: [`TERRA2136_PLAY_v0.95.0.html`](./TERRA2136_PLAY_v0.95.0.html)

Игра работает без сервера, аккаунтов и сторонних библиотек. Прогресс сохраняется локально в браузере.

### Локально через HTTP

Если браузер капризничает с локальным запуском файлов, можно поднять простой сервер:

```bash
python3 -m http.server 8000
```

После этого открыть:

```text
http://localhost:8000/
```

---

## Архитектура проекта

```text
.
├── index.html                        # landing page проекта
├── TERRA2136_PLAY_v0.95.0.html       # готовая игровая сборка
├── parts/                            # исходники, из которых собирается игра
│   ├── markup/                      # каркас меню, боя и модалок
│   ├── css/                         # стили интерфейса и слой полировки
│   ├── ui/                          # навигация, экранные модули, HUD
│   ├── game/                        # логика кампании, прогресс и симуляция
│   ├── render/                      # рендер и визуальные эффекты
│   ├── engine/                      # игровой и визуальный runtime
│   └── data/                        # конфиги, анимации, ассеты, модели
├── tools/                            # split / build / check / patch
├── qa/                               # автоматическая QA-валидация
├── patches/                          # версионные патчи и фиксы
├── docs/                             # roadmap, changelog, audit, notes
├── CLAUDE.md                         # правила разработки и инварианты
├── PROMPTS.md                        # шаблоны задач и постановок
├── REWARDS_REVIEW.md                 # анализ экономики и наград
├── README.md                         # это описание проекта
└── .github/                          # GitHub конфигурация и workflow
```

### Как всё устроено

- `tools/build.py` собирает игру обратно из `parts/` в единый HTML-файл.
- `tools/check.py` прогоняет синтаксический контроль всех JS-блоков через `node --check`.
- `qa/qa.py` проверяет меню, интерфейс, размеры кнопок, контраст, tiny text, горизонтальный overflow и smoke-test боя.
- `game/content-sim.js` и `game/progress.js` отвечают за правила кампании, экономику и локальное состояние игры.

---

## Сборка и QA

### Требования

- Python 3.11+
- Node.js 20+
- Git
- Playwright для автоматической проверки UI

### Сборка

```bash
python3 tools/build.py parts/ dist/TERRA2136_PLAY.html
```

Если исходники ещё не разложены по `parts/`:

```bash
python3 tools/split.py TERRA2136_PLAY_v0.95.0.html parts/
```

### Проверка синтаксиса

```bash
python3 tools/check.py dist/TERRA2136_PLAY.html
```

### QA-имитация интерфейса

```bash
python3 -m pip install playwright
python3 -m playwright install chromium

python3 qa/qa.py dist/TERRA2136_PLAY.html --out qa-out --no-battle
python3 qa/qa.py dist/TERRA2136_PLAY.html --out qa-out --battle-only --viewports mobile
```

QA проверяет:

- запуск основного меню;
- читаемость и размеры элементов;
- отсутствие горизонтального overflow;
- корректность работы battle smoke test;
- устойчивость UI на мобильных и desktop-разрешениях.

---

## Документация и разработка

- [`docs/ROADMAP.md`](./docs/ROADMAP.md) — план развития до `1.0.0`
- [`docs/CHANGELOG.md`](./docs/CHANGELOG.md) — лог изменений и релизов
- [`docs/AUDIT.md`](./docs/AUDIT.md) — аудит UX и технических решений
- [`docs/REWARDS_REVIEW.md`](./docs/REWARDS_REVIEW.md) — экономика и награды
- [`CLAUDE.md`](./CLAUDE.md) — правила и инварианты проекта
- [`PROMPTS.md`](./PROMPTS.md) — постановки задач и рабочие шаблоны

### Принципы разработки

- меняем исходники в `parts/`, а не готовую сборку;
- одна задача — одна тема;
- новые UI-правила пишем в финальный слой `css/10-polish95.css`;
- баланс меняется только по отдельной задаче и документируется в changelog;
- версии задаются в одном месте и не разрастаются по коду;
- игра остаётся офлайн и автономной по дизайну.

---

## Статус проекта

| Компонент | Статус |
|---|---|
| Офлайн запуск | ✅ Готово |
| Сборка в один HTML | ✅ Готово |
| Мобильный UI | ✅ QA-проверяется |
| Боевая логика | ✅ Играбельно |
| Версия `0.95.0` | ✅ В работе |
| Следующий этап (`0.96.0`) | 🛠️ HUD боя |
| Релиз `1.0.0` | 🗺️ В дорожной карте |

---

<p align="center">
  <sub>Made for Mars. Built for play. Engineered for offline.</sub>
</p>

<div align="center">
  <strong>TERRA 2136 · Desert Stryke</strong>
</div>
