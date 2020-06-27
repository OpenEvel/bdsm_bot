cd ..
IF EXIST venv rd /s /q venv
python -m venv venv
venv\Scripts\pip install --upgrade pip
venv\Scripts\pip install -r ./set_env/requirements.txt
git update-index --assume-unchanged config.py
cd set_env