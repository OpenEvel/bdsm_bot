import config
from enum import Enum
from vedis import Vedis # для работы с хранилищем состояний

class States(Enum):
    START_ENTER   = '0'
    ENTER_PASSWOD = '1'
    ENTER_COMPANY = '2'
    AUTHORIZATED  = '3'

def get_current_state(user_id):
    """
    Пытаемся узнать из базы состояний "состояние" пользователя
    """
    with Vedis(config.DB_STATES) as db:
        try:
            state = db[user_id].decode()
        except KeyError: # если такого ключа не оказалось
            # берём значение по умолчанию
            state = States.START_ENTER.value
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
