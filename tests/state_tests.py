# -*- coding: utf-8 -*-
import sys
import os
import unittest
import sqlite3
# Делаем видимыми модули уровнем выше для наших тестов
sys.path.append('..') # в vs code - не нужно
# теперь можем импортировать модуль для работы с админами
from logic.statesworker import States, StatesWorker, get_state, set_state, IDError 
from tools import full_path

# имя тестовой базы данных
dbname = full_path(__file__, 'test_db')

class TestState(unittest.TestCase):
    def setUp(self):
        conn = sqlite3.connect(dbname + os.extsep + 'db')
        sql_file = open(dbname + os.extsep + 'sql', encoding='utf-8')
        conn.executescript(sql_file.read())
        sql_file.close()
        conn.close()

    def tearDown(self):
        os.remove(dbname + os.extsep + 'db')

    def test_get_state_user_not_in_table(self):
        """Правильно ли получает пользователя, которого НЕТ в таблице"""
        state = get_state(2, database=dbname + os.extsep + 'db')
        self.assertEqual(States.START_ENTER, state, "Состояние пользователя, которого нет в таблице States.START_ENTER")
    
    def test_get_state_user_in_table(self):
        """Правильно ли получает пользователя, который ЕСТЬ в таблице"""
        state = get_state(1, database=dbname + os.extsep + 'db')
        self.assertEqual(States.AUTHORIZATED, state, "Состояние пользователя, который есть в таблице States.AUTHORIZATED")

    def test_set_state_for_new_user(self):
        """Правильно ли задаёт состояние для нового пользователя"""
        set_state(3, States.AUTHORIZATED, database=dbname + os.extsep + 'db')
        state = get_state(3, database=dbname + os.extsep + 'db')
        self.assertEqual(States.AUTHORIZATED, state, "Состояние пользователя должно быть States.AUTHORIZATED")
    
if __name__ == "__main__":
    unittest.main()
