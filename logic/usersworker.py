# -*- coding: utf-8 -*-
import config
import abc              # для создания абстрактных классов
import sqlite3          # Для подключения к БД

class User:
    """
    Класс для пользователя
    Предоставляет свойства которыми должен обладать пользователь
    Полеезен в ошибках, подсветке кода и при возврате данных о пользователе из функций
    """

    def __init__(self, id, username, first_name, last_name):
        self.id = id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name

class UsersWorker(abc.ABC):
    """Абстрактный класс для работы с таблицами пользователй в базе sqlite"""

    # методы которые не надо переопределять
    def __init__(self, database=config.DB_WORK):
        """При создании экземпляра принимает название файла БД"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def close(self):
        """Закрываем текущее соединение с БД"""
        self.connection.close()
    
    @abc.abstractclassmethod
    def get_ids(self):
        """Получить список всех id в таблице"""
        pass

    @abc.abstractclassmethod
    def _is(self, user_id):
        """Есть ли пользователь с user_id внутри таблицы"""
        pass

    @abc.abstractclassmethod
    def add(self, user: User):
        """Добавить пользователя в таблицу"""
        pass
    
    @abc.abstractclassmethod
    def get(self, user_id):
        """
        Получить пользователя и таблицы по уникальном
        идентификатору user_id
        """
        pass

    @abc.abstractclassmethod
    def remove(self, user:User or int):
        """
        Удалить пользователя из таблицы
        user - либо объект User, либо целое число - id пользователя
        """
        pass

    @abc.abstractclassmethod
    def count(self):
        """Количество записей в таблице"""
        pass
