# -*- coding: utf-8 -*-
import config
import abc              # для создания абстрактных классов
import sqlite3          # Для подключения к БД
from vedis import Vedis # для работы с хранилищем состояний

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

class DBWorker(abc.ABC):
    """Абстрактный класс для работы с БД sqlite"""

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
    def count(self):
        """Количество записей в таблице"""
        pass


# Работаем теперь с СОСТОЯНИЯМИ пользоватлей
def get_current_state(user_id):
    """
    Пытаемся узнать из базы состояний "состояние" пользователя
    """
    with Vedis(config.DB_STATES) as db:
        try:
            state = db[user_id].decode()
        except KeyError: # если такого ключа не оказалось
            # берём значение по умолчанию
            state = config.States.START_ENTER.value
        return state


def set_state(user_id, value):
    """
    Сохраняем текущее «состояние» пользователя в нашу базу состояний
    """
    with Vedis(config.DB_STATES) as db:
        try:
            db[user_id] = value
            return True
        except:
            # тут желательно как-то обработать ситуацию
            # но врядли что-то такое случится
            return False