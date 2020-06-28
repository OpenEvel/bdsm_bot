#!/bin/bash
echo ------------------starting----------------------
# На всякий случай удаляем предыдущее окружение
rm -fr ../venv >> install.log
echo making 'venv' directory
python3 -m venv ../venv >> install.log
echo upgrading pip
../venv/bin/pip install --upgrade pip >> install.log 2>> erorr_install.log
echo "pip installing requirements(python libraries)"
../venv/bin/pip install -r ./requirements.txt >> install.log 2>> erorr_install.log
# Чтобы изменения в файле config не было видно git и мы случайно его не закомментили в ветку
echo making 'config.py' file invisible to git
git update-index --assume-unchanged ../config.py >> install.log

echo deliting log files
rm -f ./*.log
echo ------------------complited----------------------