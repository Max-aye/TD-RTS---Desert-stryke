---
name: terra-pipeline
description: Разбор, правка, патчи и сборка 43-мегабайтного HTML TERRA 2136 (split → patch → build → check). Используй этот навык при любой правке игры, при подготовке новой версии, переносе правок между версиями и всякий раз, когда нужно найти, где в игре лежит код экрана, стиля, модели или баланса — даже если пользователь просто пишет «поправь в игре…».
---

# Конвейер TERRA 2136

Исходник игры — один HTML. Редактировать его напрямую нельзя: файл огромный, а 90 % его — base64-данные. Всегда работай с `parts/`.

## Первый запуск на новой версии HTML

```
python3 tools/split.py TERRA2136_PLAY_vX.html parts/
python3 tools/build.py parts/ /tmp/roundtrip.html --verify   # должно быть "byte-identical"
cd parts && git init && git add -A && git commit -m "vX baseline"   # история правок = git
```
Если `split.py` пишет «anchor found N times», значит в новой версии сдвинулась граница модуля: найди новую строку-якорь (`grep -n`) и обнови `SCRIPT_PLAN` в `tools/split.py`.

## Где что лежит

Таблица частей — в `CLAUDE.md`. Быстрый поиск:
- экран меню → `grep -n "route==='<route>'" parts/ui/controller.js`, шаблон → `grep -n "function <name>(ctx" parts/ui/views.js`
- стиль класса → `grep -n "\.<class>" parts/css/*.css` (последний файл в manifest побеждает при равной специфичности)
- карта/юнит/баланс → `grep -o '"id":"<id>"[^}]*' parts/data/design-config.js`
- модель → `grep -o "TERRA_MODELS\[.<model-id>.\]" parts/data/assets-models.js`

## Патч-набор (переносимые правки)

`patches/vX_Y_Z/spec.py`:
```python
VERSION = '0.96.0'
EDITS = [dict(file='ui/controller.js', old='точный старый текст', new='новый текст', count=1, why='что чиним')]
NEW_PARTS = [dict(file='css/11-polish96.css', source='polish96.css', after='css/10-polish95.css', glue_before='</style><style>')]
```
`python3 tools/patch.py patches/vX_Y_Z parts/` — либо применяется целиком, либо не пишет ничего. Повторный запуск безопасен. В `new` можно вставлять `{{FILE:имя}}` и `{{VERSION}}`.

## Обязательный цикл после правки

```
python3 tools/build.py parts/ dist/TERRA2136_PLAY.html
python3 tools/check.py dist/TERRA2136_PLAY.html
python3 qa/qa.py dist/TERRA2136_PLAY.html --out qa-out --no-battle
```
Затем навык `terra-visual-check`, если менялось то, что видно.

## Релиз

1. `ui/version95.js` (или `{{VERSION}}` в патче), `<title>` и штамп в `markup/body.html` — одна и та же версия.
2. Запись в `docs/CHANGELOG.md`: что изменилось для игрока, что для кода, результаты QA.
3. `python3 tools/build.py parts/ TERRA2136_PLAY_vX_Y_Z.html`.
