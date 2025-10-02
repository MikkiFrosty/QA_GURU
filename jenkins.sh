#!/usr/bin/env bash
set -e

python3 -m venv .venv
. .venv/bin/activate
pip install -U pip
pip install -r requirements.txt

pytest -v || true

ALLURE_CLI="/home/jenkins/tools/ru.yandex.qatools.allure.jenkins.tools.AllureCommandlineInstallation/allure_2.17.2/bin/allure"
$ALLURE_CLI generate -c -o allure-report
