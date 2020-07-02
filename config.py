# -*- coding: utf-8 -*-
from enum import Enum
import os

def full_path(file_var, relative_path):
    """
    file_var: переменная __file__ модуля, в которм используется эта функция
    relative_path: относительный путь относительно папки модуля
    возвращает полный путь относительно директроии, в которой находится модуль
    """
    module_dir = os.path.split(os.path.abspath(file_var))[0]
    return os.path.normpath(os.path.join(module_dir, relative_path))

TOKEN = 'YOUR_TOKEN'
ADMIN_ID = 'YUOR_ID' # Должно быть число а не строка
DB_WORK = full_path(__file__, 'bases/work.db')       # Файл с базой данных о пользователях
DB_STATES = full_path(__file__, 'bases/states.vdb')  # Файл с базой данных о состояних

class States(Enum):
    START_ENTER   = '0'
    ENTER_PASSWOD = '1'
    ENTER_COMPANY = '2'
    AUTHORIZATED  = '3'
