# -*- coding: utf-8 -*-
import sys
import os
import unittest
import sqlite3
# Делаем видимыми модули уровнем выше для наших тестов
module_dir = os.path.split(os.path.abspath(__file__))[0]
workspace_dir = os.path.normpath(os.path.join(module_dir, os.pardir))
sys.path.append(workspace_dir)
# теперь можем импортировать модуль для работы с админами
from logic.statesworker import States, StatesWorker, get_state, set_state, IDError 
from tools import full_path

# имя тестовой базы данных
DB_NAME = full_path(__file__, 'test_db')
REAL_DB = DB_NAME + os.extsep + 'db'
SQL_DB = DB_NAME+ os.extsep + 'sql'

class TestState(unittest.TestCase):
    def setUp(self):

        conn = sqlite3.connect(REAL_DB)
        sql_file = open(SQL_DB, encoding='utf-8')
        conn.executescript(sql_file.read())
        sql_file.close()
        conn.close()

    def tearDown(self):
        os.remove(REAL_DB)

    def test_get_state_user_not_in_table(self):
        """Правильно ли получает пользователя, которого НЕТ в таблице"""
        state = get_state(2, database=REAL_DB)
        self.assertEqual(States.START_ENTER, state, "Состояние пользователя, которого нет в таблице States.START_ENTER")
    
    def test_get_state_user_in_table(self):
        """Правильно ли получает пользователя, который ЕСТЬ в таблице"""
        state = get_state(1, database=REAL_DB)
        self.assertEqual(States.AUTHORIZATED, state, "Состояние пользователя, который есть в таблице States.AUTHORIZATED")

    def test_set_state_for_new_user(self):
        """Правильно ли задаёт состояние для нового пользователя"""
        set_state(3, States.AUTHORIZATED, database=REAL_DB)
        state = get_state(3, database=REAL_DB)
        self.assertEqual(States.AUTHORIZATED, state, "Состояние пользователя должно быть States.AUTHORIZATED")
    
if __name__ == "__main__":
    unittest.main()
