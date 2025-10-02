# Дипломный проект по автоматизации тестирования Ozon (калькулятор вкладов)

## О проекте
Этот проект является дипломной работой по курсу QA.GURU.  
Проект представляет собой фреймворк для автоматизации тестирования **калькулятора вкладов на сайте Ozon**.

## Технологии и инструменты
- Python 3.10+
- Pytest
- Selenium / Selene
- Allure Report
- Selenoid (remote WebDriver)
- GitHub + Jenkins

<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="50" height="50"/> 
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/selenium/selenium-original.svg" width="50" height="50"/> 
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/pytest/pytest-original.svg" width="50" height="50"/> 
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg" width="50" height="50"/> 

## Покрытый функционал
Автотестами покрыты основные сценарии работы калькулятора вкладов:
- ✅ Валидный ввод суммы и срока вклада  
- ✅ Минимальное значение суммы  
- ✅ Ошибка при вводе суммы меньше минимума  
- ✅ Ошибка при вводе невалидных символов  
- ✅ Smoke-проверка отображения формы  
- ✅ Проверка изменения срока вклада  
- ✅ Проверка влияния капитализации на расчёт прибыли  

Итого: 7 UI-тестов.

## Структура проекта
- `tests/` — автотесты  
- `tests/pages/` — PageObject для калькулятора вкладов  
- `tests/models/` — модели данных (Deposit_class и локаторы)  
- `tests/resources/` — ресурсы для тестов (если будут)  
- `utils/` — утилиты для вложений (attach для Allure)  
- `tests/conftest.py` — фикстуры для запуска тестов  

## Запуск тестов
1. Клонировать репозиторий:
   ```bash
   git clone <ссылка-на-репозиторий>
   cd <папка-проекта>
   ```
2. Установить зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Запустить тесты с генерацией Allure-результатов:
   ```bash
   pytest -v --alluredir=allure-results
   allure serve allure-results
   ```

## Интеграции
- Jenkins Job:  
- Allure Report в Jenkins: 
- Telegram уведомления: 

---
