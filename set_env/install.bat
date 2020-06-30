@echo off
echo ------------------starting----------------------
IF EXIST ..\venv rd /s /q ..\venv >> install.log
echo making 'venv' directory
python -m venv ..\venv >> install.log
echo upgrading pip
..\venv\Scripts\pip install --upgrade pip --user >> install.log 2>> erorr_install.log
echo pip installing requirements(python libraries)
..\venv\Scripts\pip install -r .\requirements.txt >> install.log 2>> erorr_install.log
echo making 'config.py' file invisible to git
git update-index --assume-unchanged ..\config.py  >> install.log

echo deliting log files
del /q .\*.log
echo ------------------complited----------------------