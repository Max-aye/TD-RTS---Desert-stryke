<div align="right">

**Русский** &nbsp; / &nbsp; [English](./README.md)

</div>

<p align="center">
  <img src="./docs/media/terra2136-cover-frontier.jpg" width="1200" alt="TERRA 2136 — Desert Stryke. Промо-арт колониального рубежа.">
</p>

<div align="center">

# TERRA 2136 · Desert Stryke

### Построй рубеж. Перехвати инициативу. Вернись сильнее.

Трёхмерная **tower offense × RTS** с автоматическими отрядами
и коллекцией боевых карт — в одном HTML-файле.

<p>
  <img src="./docs/media/badge-render.svg" height="28" alt="WEBGL 2">
  <img src="./docs/media/badge-format.svg" height="28" alt="SINGLE HTML">
  <img src="./docs/media/badge-play.svg" height="28" alt="OFFLINE">
  <img src="./docs/media/badge-status.svg" height="28" alt="IN DEVELOPMENT">
</p>

[**Сборка игры ↗**](./TERRA2136_PLAY_v0.99.2.html) &nbsp; · &nbsp; [Быстрый старт](#quick-start) &nbsp; · &nbsp; [Арсенал](#arsenal) &nbsp; · &nbsp; [Разработка](#development)

</div>

<table width="100%">
  <tr>
    <td width="25%" align="center"><h3>50</h3>операций кампании</td>
    <td width="25%" align="center"><h3>82</h3>боевые карты</td>
    <td width="25%" align="center"><h3>T1–T6</h3>боевые улучшения</td>
    <td width="25%" align="center"><h3>30</h3>дней наград</td>
  </tr>
</table>

## Тактика вместо микроконтроля

Разверни производства и оборону вдоль общего маршрута. Три поста с тремя площадками на каждом, автоматические подкрепления и центральный маяк превращают каждый бой в соревнование по времени и позиции.

Подбери колоду из **6 карт и 2 умений поддержки**. Удержи штаб, прорви оборону или выведи транспорт с колонистами — цель меняется от операции к операции.

<p align="center"><strong>Колода → посты → бой → награды → улучшения</strong></p>

## Каждая вылазка делает арсенал сильнее

<table width="100%">
<tr>
  <td width="50%"><strong>Кампания и вылазки</strong><br><br>50 основных операций, ресурсные задания, полигон, недельные операции и экспедиционные маршруты.</td>
  <td width="50%"><strong>Коллекция и развитие</strong><br><br>Четыре редкости карт, опыт, ранги, специализации, модули и сохранённые комплекты.</td>
</tr>
<tr>
  <td width="50%"><strong>Награды за игру</strong><br><br>Полевая добыча, контейнеры снабжения, задания и календарь наград на 30 дней.</td>
  <td width="50%"><strong>Штаб и ангар</strong><br><br>Сбор колоды, просмотр моделей, планирование улучшений и боевые отчёты.</td>
</tr>
</table>

## Мир TERRA 2136

<table width="100%">
<tr>
  <td width="50%" align="center"><a href="./docs/media/ingame-menu.webp"><img src="./docs/media/ingame-menu.webp" width="600" alt="Купол колонии среди гор — игровой арт штаба."></a><br><sub>Штаб</sub></td>
  <td width="50%" align="center"><a href="./docs/media/ingame-expedition.webp"><img src="./docs/media/ingame-expedition.webp" width="600" alt="Экспедиция у залежей минералов — боевой арт."></a><br><sub>Экспедиция</sub></td>
</tr>
</table>
<p align="center"><sub>Игровые иллюстрации из сборки.</sub></p>

<a id="arsenal"></a>

## Собери свой арсенал

Пехота, бронетехника, авиация и оборонительные сооружения. **Авангард · Кузня · Кайрос** — три фракционных набора для передовой.

<table width="100%">
<tr>
  <td width="50%" align="center"><img src="./docs/media/arsenal-armor.webp" width="220" alt="Осадный танк"><br><strong>Осадный танк</strong><br><sub>БРОНЕТЕХНИКА</sub></td>
  <td width="50%" align="center"><img src="./docs/media/arsenal-turret.webp" width="220" alt="Автопушка"><br><strong>Автопушка</strong><br><sub>ОБОРОНА</sub></td>
</tr>
<tr>
  <td width="50%" align="center"><img src="./docs/media/arsenal-interceptor.webp" width="220" alt="Перехватчик"><br><strong>Перехватчик</strong><br><sub>АВИАЦИЯ</sub></td>
  <td width="50%" align="center"><img src="./docs/media/arsenal-ward.webp" width="220" alt="Защитная установка"><br><strong>Защитная установка</strong><br><sub>ПОДДЕРЖКА</sub></td>
</tr>
</table>

<a id="quick-start"></a>

## Начни играть

1. Открой [HTML-сборку](./TERRA2136_PLAY_v0.99.2.html) и нажми **Download raw file**.
2. Запусти скачанный файл в браузере с **WebGL 2**.
3. Выбери колоду и начни первую операцию.

**Без установки, аккаунта и отдельного сервера.** Все игровые ресурсы уже внутри файла. На Android открывай HTML через браузер, а не через просмотрщик документов. Интерфейс игры — на русском языке.

<details>
<summary><strong>Управление и сохранения</strong></summary>

**Телефон:** касание — выбор площадки или постройки; перетаскивание — камера; два пальца — масштаб. Выбери умение поддержки, затем коснись точки на поле.

| Действие | Клавиши / мышь |
| --- | --- |
| Выбор · камера · масштаб | Левый щелчок · перетаскивание · колесо |
| Выбрать пост · открыть строительство | `1` `2` `3` · `B` |
| Карта в открытой панели строительства | `Q` `W` `E` `R` `T` `Y` |
| Приблизить пост · открыть цели | `F` · `O` |
| Пауза · отмена / закрытие | `Пробел` · `Esc` |

Буквенные клавиши — в английской раскладке.

Прогресс сохраняется локально. В настройках доступны **экспорт и импорт JSON**. Импорт заменяет текущий профиль — перед импортом сделай резервный экспорт.

При проблемах с WebGL проверь аппаратное ускорение браузера. На слабом устройстве снизь качество и масштаб боя. Локальное открытие и хранение данных на Android зависят от браузера.

</details>

<a id="development"></a>

## Разработка

**JavaScript · HTML/CSS · собственный WebGL 2-рендерер.**
Фиксированный шаг симуляции, встроенные ресурсы, адаптивное разрешение и интерфейс для портретного и альбомного режима.

[Сборка и структура проекта](./docs/presentation/DEVELOPMENT.md) · [Дорожная карта](./docs/ROADMAP.md) · [Изменения](./docs/CHANGELOG.md) · [Правила проекта](./CLAUDE.md)

### Инструменты

```bash
python3 tools/split.py TERRA2136_PLAY_v0.99.2.html parts/
python3 tools/build.py parts/ dist/TERRA2136_PLAY.html
python3 tools/check.py dist/TERRA2136_PLAY.html
python3 qa/qa.py dist/TERRA2136_PLAY.html --out qa-out --no-battle
python3 qa/qa.py dist/TERRA2136_PLAY.html --out qa-out --battle-only --viewports mobile
```

В Windows вместо `python3` используй `py`.

---

<div align="center">

**Один файл. Твой рубеж. Твоя тактика.**

Проект **[Max-aye](https://github.com/Max-aye)** · [Сообщить об ошибке](https://github.com/Max-aye/TD-RTS---Desert-stryke/issues) · [Источники медиа](./docs/presentation/MEDIA.md)

</div>
