# Ozon Deposit — демо‑проект по автоматизации (Web)

<p align="center">
<img title="Allure Overview" src="images/allure_overview.png">
</p>

## Содержание
> ➠ [Технологический стек](#технологический-стек)  
> ➠ [Покрытый функционал](#покрытый-функционал)  
> ➠ [Сборка в Jenkins](#jenkins)  
> ➠ [Запуск из терминала](#запуск-из-терминала)  
> ➠ [Allure Report](#allure-report)  
> ➠ [Allure TestOps](#allure-testops)  
> ➠ [Уведомления в Telegram](#уведомления-в-telegram)  
> ➠ [Пример видео прохождения тестов](#пример-видео-прохождения-тестов)

## Технологический стек
<p align="center">
<img src="images/logos/python-original.svg" width="50" height="50" alt="Python"/>
<img src="images/logos/pytest.png" width="50" height="50" alt="Pytest"/>
<img src="images/logos/selenium.png" width="50" height="50" alt="Selenium/Selene"/>
<img src="images/logos/jenkins.png" width="50" height="50" alt="Jenkins"/>
<img src="images/logos/allure_report.png" width="50" height="50" alt="Allure Report"/>
<img src="images/logos/allure_testops.png" width="50" height="50" alt="Allure TestOps"/>
<img src="images/logos/tg.png" width="50" height="50" alt="Telegram"/>
<img src="images/logos/github.png" width="50" height="50" alt="GitHub"/>
</p>

В проекте автотесты написаны на <code>Python + Pytest</code> с использованием <code>Selenium/Selene</code> для UI. 
Сборки запускаются в <code>Jenkins</code>, отчётность — <code>Allure Report</code> и <code>Allure TestOps</code>, уведомления идут в <code>Telegram</code>.

## Покрытый функционал
> UI‑тесты формы вклада <strong>Ozon Deposit</strong>

- [x] Валидный депозит — корректное заполнение формы
- [x] Минимальная сумма — ровно порог
- [x] Сумма ниже минимума — валидационная ошибка
- [x] Ввод нечисловых символов
- [x] Смена срока на 3 месяца — обновление бейджа
- [x] Отображение формы (smoke)
- [x] Капитализация — переключатель влияет на расчёт прибыли

## Jenkins
<p align="center">
<img src="images/jenkins_runs.png" alt="Jenkins runs">
</p>

### Параметризованный запуск (пример)
В Jenkins выбирается <code>Build with Parameters</code>: окружение, браузер, версия. После прогона ссылка на Allure доступна из сборки.

## Запуск из терминала
Локально:
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest -m "ui" -q
```

Генерация отчёта локально:
```bash
allure serve allure-results
```

## Allure Report
### Основной отчёт
<p align="center">
<img src="images/allure_overview.png" alt="Allure overview">
</p>

### Графики
<p align="center">
<img src="images/allure_graph.png" alt="Allure graphs">
</p>

## Allure TestOps
### Список кейсов
<p align="center">
<img src="images/testops_cases.png" alt="TestOps cases">
</p>

### Dashboard
<p align="center">
<img src="images/testops_dash.png" alt="TestOps dashboard">
</p>

## Уведомления в Telegram
<p align="center">
<img src="images/tg_notification.png" alt="Telegram notification" height="260">
</p>

## Пример видео прохождения тестов
<p align="center">
<img src="images/ozon_autotest.gif" alt="Autotest video gif">
</p>
