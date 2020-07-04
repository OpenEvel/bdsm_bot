# -*- coding: utf-8 -*-
"""
Модуль, в котором реализована логика работы с таблицей админов в базе данных
"""
import sqlite3
from ..usersworker import UsersWorker, User

class Admin(User):
    """Класс Представляющий одного админа"""

    def __repr__(self):
        """
        Полезен при отладки - выводит информацию об админе в виде строки
        """
        return f'<Admin id={self.id} name={self.username}>'

class AdminsWorker(UsersWorker):
    """Работает с админами в базе данных"""
    TABLE = 'admins' # название таблицы с админами в БД

    def get_ids(self):
        """Получить список id всех админов"""
        with self.connection:
            rows = self.cursor.execute(f"SELECT id FROM {AdminsWorker.TABLE}").fetchall()
        return [row[0] for row in rows]
    
    def _is(self, user_id):
        """Является ли пользователь с user_id админом"""
        # пока подойдёт стандартная, представленная в абстрактном классе
        return user_id in self.get_ids()
    
    def add(self, user: User):
        """Добавть пользователя в список админов"""
        # пытаемся его туда добавить
        try:
            with self.connection:
                self.cursor.execute(f"INSERT INTO {AdminsWorker.TABLE} VALUES (?,?,?,?)", 
                                    (user.id,
                                     user.username,
                                     user.first_name,
                                     user.last_name))
        except sqlite3.DatabaseError as err:
            # не смогли добавить пользователя
            # Выводим сообщение об ошибке
            print("Error ", err)
            return False
        else:
            # пользователь успешно добавлен
            return True
    
    def get(self, user_id):
        """
        Врнуть одного админа из таблицы по его user_id
        возвращает экземпляр класса Admin,
        который обладает всеми сопутствующими свойствами
        """
        with self.connection:
            admin = self.cursor.execute(f"SELECT * FROM {AdminsWorker.TABLE} WHERE id=?", (user_id,)).fetchone()

        # при помощи конструкции *admin - мы можем передавать значения из списка
        # в функцию __init__ класса Admin как по одному
        # то есть Admin(admin[0], admin[1], admin[2], admin[3]) - то же самое но сокращённей
        return Admin(*admin)
    
    def remove(self, user:User or int):
        """
        Удалить админа из таблицы
        user - либо объект User, либо целое число - id пользователя
        """
        # Получаем id пользователя
        if not getattr(user, 'id', None):
            user_id = user
        else:
            user_id = user.id
        
        if not self._is(user_id):
            # Пользователь не админ, значит удалять его и не надо
            return False
        else:
            with self.connection:
                self.cursor.execute(f"DELETE FROM {AdminsWorker.TABLE} WHERE id=?", (user_id,))
            # Админа удалили все прошло успешно
            return True
    
    def count(self):
        """Получаем количество админов в таблице"""
        with self.connection:
            rows = self.cursor.execute(f"SELECT * FROM {AdminsWorker.TABLE}").fetchall()
            # rows = self.get_ids() # можно было и так
        return len(rows)
    
    def get_all_list(self):
        """
        Получить всех админов из таблицы в виде списка
        один админ(элемент списка) сам тоже является КОРТЕЖЕМ
        """
        with self.connection:
            rows = self.cursor.execute(f"SELECT * FROM {AdminsWorker.TABLE}").fetchall()
        return rows
    
    def get_all(self):
        """
        Получить всех админов из таблицы в виде списка ОБЪЕКТОВ
        Один админ - экземпляр класса Admin
        """
        return [Admin(*admin) for admin in self.get_all_list()]
