#!/bin/bash
cd ..
rm -fr venv   # На всякий случай удаляем предыдущее окружение
python3 -m venv venv
source ./venv/bin/activate
pip install --upgrade pip
pip install -r ./set_env/requirements.txt

# Чтобы изменения в файле config не было видно git и мы случайно его не закомментили в ветку
git update-index --assume-unchanged config.py