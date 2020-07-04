# -*- coding: utf-8 -*-
import sys
import os
import unittest
import sqlite3
# Делаем видимыми модули уровнем выше для наших тестов
sys.path.append('..') # в vs code - не нужно
# теперь можем импортировать модуль для работы с админами
from logic import admins
from tools import full_path

# имя тестовой базы данных
dbname = full_path(__file__, 'test_db')

def isSame(a1: admins.tabler.Admin, a2: admins.tabler.Admin):
    """Являются ли админы одинаковыми"""
    id = a1.id == a2.id
    username = a1.username == a2.username
    first_name = a1.first_name == a2.first_name
    last_name = a1.last_name == a2.last_name

    answer = id and username and first_name and last_name
    return answer


class TestAdmin(unittest.TestCase):
    def setUp(self):
        conn = sqlite3.connect(dbname + os.extsep + 'db')
        sql_file = open(dbname + os.extsep + 'sql', encoding='utf-8')
        conn.executescript(sql_file.read())
        sql_file.close()
        conn.close()

        self.adminer = admins.tabler.AdminsWorker(dbname + os.extsep + 'db')

    def tearDown(self):
        self.adminer.close()
        os.remove(dbname + os.extsep + 'db')

    def test_get_ids(self):
        """Правильно ли возвращает id админов"""
        answer = self.adminer.get_ids()
        self.assertEqual(answer, [1, 2, 3], "Должно быть [1, 2, 3]")
    
    def test_its_me(self):
        """Пользователь ЕСТЬ в базе админов"""
        answer = self.adminer._is(1)
        self.assertEqual(answer, True, 'Пользователь с id=1 должен быть внутри таблицы')
    
    def test_its_not_me(self):
        """Пользователя НЕТ в базе админов"""
        answer = self.adminer._is(4)
        self.assertEqual(answer, False, 'Пользователь с id=4 НЕ должен быть внутри таблицы')

    def test_add_admin(self):
        """Добавление админа в таблицу"""
        # создаём одного админа
        admin = admins.tabler.Admin(777, 'lol', 'lol', 'lol')
        # добавляем его в таблицу с админами
        self.adminer.add(admin)
        # проверяем есть он там
        self.assertEqual(self.adminer._is(admin.id), True, 'Ошибка добавления админа в таблицу')

    def test_count(self):
        """Вычисление количества админов в таблице"""
        self.assertEqual(self.adminer.count(), 3, 'Админов должно быть 3')
    
    def test_get_one_admin(self):
        """Возвращение админа из таблицы"""
        admin_real = admins.tabler.Admin(1, 'a', 'aa', 'aaa')
        admin_table = self.adminer.get(1)

        answer = isSame(admin_real, admin_table)
        self.assertEqual(answer, True)
    
    def test_get_all_list(self):
        """Возвращение админов в виде списка кортежей"""
        list_fields = self.adminer.get_all_list()
        right_list = [(1, 'a', 'aa', 'aaa'),
                      (2, 'b', 'bb', 'bbb'),
                      (3, 'c', 'cc', 'ccc')]
        self.assertEqual(list_fields, right_list)
    
    def test_get_all(self):
        """Возвращение админов виде списка объектов класса Admin"""
        table_admins = self.adminer.get_all()

        right_list = [(1, 'a', 'aa', 'aaa'),
                      (2, 'b', 'bb', 'bbb'),
                      (3, 'c', 'cc', 'ccc')]
        real_admins = [admins.tabler.Admin(*admin) for admin in right_list]

        a0 = isSame(table_admins[0], real_admins[0])
        a1 = isSame(table_admins[1], real_admins[1])
        a2 = isSame(table_admins[2], real_admins[2])

        answer = a0 and a1 and a2
        self.assertEqual(answer, True, "Админы не совпали")

    def test_del_admin_by_id(self):
        """Удалить админа из таблицы по id"""

        count = self.adminer.remove(2)
        count+= self.adminer.remove(3)
        count+= self.adminer.remove(1)

        self.assertEqual(count, 3, "Успешное удаление должно было случиться 3 раза")

    def test_del_admin_by_object(self):
        """Удалить админа из таблицы, когда передаётся объект Admin"""
        list_admins = [(1, 'a', 'aa', 'aaa'),
                      (2, 'b', 'bb', 'bbb'),
                      (3, 'c', 'cc', 'ccc')]
        a1, a2, a3 = [admins.tabler.Admin(*admin) for admin in list_admins]

        count = self.adminer.remove(a2)
        count+= self.adminer.remove(a3)
        count+= self.adminer.remove(a1)

        self.assertEqual(count, 3, "Успешное удаление должно было случиться 3 раза")

    def test_del_admin_who_is_not_in_table(self):
        """Удалить админа из таблицы по id"""

        answer = self.adminer.remove(4)

        self.assertEqual(answer, False, "В таблице нет такого админа")


if __name__ == "__main__":
    unittest.main()
