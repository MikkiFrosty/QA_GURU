# 🎓 QA.GURU WB Project

*Небольшой проект по автоматизации Wildberries, по выбору ПВЗ и добавлению товара*

## О проекте

Этот проект является дипломной работой по курсу QA.GURU и представляет собой фреймворк для автоматизации тестирования "Ozone банк" (https://finance.ozon.ru/promo/deposit/landing). В реализации использованы инструменты и библиотеки:

<p  align="center">
  
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" height="100" width="100"/>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/jenkins/jenkins-original.svg" height="100" width="100"/>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/pytest/pytest-original.svg" height="100" width="100"/>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/github/github-original.svg" height="100" width="100"/>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/selenium/selenium-original.svg" height="100" width="100"/>
</p>

## <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" height="20" width="20"> Запуск тестов локально

1) Клонировать репозиторий: git clone https://github.com/MikkiFrosty/QA_GURU
2) Установить зависимости: pip install -r requirements.txt
3) Запуск тестов с генерацией отчетов Allure: pytest --alluredir=reports/allure-results

##   <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/jenkins/jenkins-original.svg" height="20" width="20"/> Создание сборки на удаленном сервере - Jenkins

1) Авторизоваться в Jenkins
2) Перейти в джобу https://jenkins.autotests.cloud/job/project_wildeberries_mozzhukhin
3) Для запуска тестов в Jenkins нажать "Build Now"


## <img width="4%" title="allure" src="data/logo/allure_report.png"> Визуализация результатов (Allure Reports и Allure TestOps)

Для просмотра результатов тестового прогона в Allure клик на соответствующую ему иконку

## <img width="4%" title="tg" src="data/logo/tg.png"> Интеграция с Telegram в Jenkins для автоматической отправки результатов тестового прогона через бота
