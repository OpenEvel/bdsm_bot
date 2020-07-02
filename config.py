# -*- coding: utf-8 -*-
from tools import full_path

TOKEN = 'YOUR_TOKEN'
ADMIN_ID = 'YUOR_ID' # Должно быть число а не строка
DB_WORK = full_path(__file__, 'bases/work.db')       # Файл с базой данных о пользователях
DB_STATES = full_path(__file__, 'bases/states.vdb')  # Файл с базой данных о состояних
