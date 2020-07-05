import config
import sqlite3
from enum import Enum

class States(Enum):
    START_ENTER   = '0'
    ENTER_PASSWOD = '1'
    ENTER_COMPANY = '2'
    AUTHORIZATED  = '3'

class IDError(IndexError):
    pass

class StatesWorker:
    """Класс для работы с состяниями пользователей в базе данных"""

    TABLE = "states" # название таблицы с состояниями в БД

    def __init__(self, database=config.DB_WORK):
        """При создании экземпляра принимает название файла БД"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
    
    def close(self):
        """Закрываем текущее соединение с БД"""
        self.connection.close()
    
    def gen_ids(self):
        """Получить объект генератоа всех id из таблицы состояний"""
        with self.connection:
            rows = self.cursor.execute(f"SELECT id FROM {StatesWorker.TABLE}").fetchall()        
        for row in rows:
            yield row[0]
    
    def __getitem__(self, user_id):
        if user_id not in self.gen_ids():
            raise IDError

        with self.connection:
            rows = self.cursor.execute(f"SELECT state FROM {StatesWorker.TABLE} WHERE id=?", (user_id,)).fetchall()
        
        value = rows[0][0][1]

        for state in States:
            if state.value == value:
                return state
      
    def __setitem__(self, user_id:int, state:States):
        # Пользователь есть в таблице
        if user_id not in self.gen_ids():
            # пытаемся добавить состояние пользователя
            with self.connection:
                self.cursor.execute(f"INSERT INTO {StatesWorker.TABLE} VALUES (?,?)", (user_id, state.value))
        else:
            # Пользователя нет в таблице
            # Обновляем состояние пользователя
            with self.connection:
                self.cursor.execute(f"UPDATE {StatesWorker.TABLE} SET state=? WHERE id=?", (state.value, user_id))
    
    def __delitem__(self, user_id):
        if user_id not in self.gen_ids():
            # Пользователь нет в таблице, значит удалять его и не надо
            return False
        else:
            with self.connection:
                self.cursor.execute(f"DELETE FROM {StatesWorker.TABLE} WHERE id=?", (user_id,))
            # Админа удалили все прошло успешно
            return True

def get_state(user_id:int):
    """Пытаемся узнать состояние пользователя"""
    stater = StatesWorker()

    try:
        state = stater[user_id]
    except IDError:
        stater[user_id] = States.START_ENTER
        return States.START_ENTER
    else:
        return state

def set_state(user_id:int, state:States):
    """Сохраняем текущее «состояние» пользователя в нашу базу состояний"""
    stater = StatesWorker()
    stater[user_id] = state
