# -*- coding: utf-8 -*-
import sys
import os
import telebot
from telebot.types import Message

import sqlite3
from utils.admins.dber import AdminWorker

config_template = """# -*- coding: utf-8 -*-
from enum import Enum

TOKEN = '{TOKEN}'
ADMIN_ID = {ADMIN_ID}
DB_WORK = 'bases/work.db'  # Файл с базой данных о пользователях
DB_STATES = 'bases/states.vdb'  # Файл с базой данных о состояних

class States(Enum):
    START_ENTER = '0'
    ENTER_PASSWOD = '1'
    ENTER_COMPANY = '2'
    AUTHORIZATED = '3'
"""

if __name__ == "__main__":
    args = sys.argv[1:]

    if '--configure' in args:
        if len(args) == 2:
            args.remove('--configure')
            TOKEN = args[0]
            bot = telebot.TeleBot(TOKEN)

            @bot.message_handler(content_types=["text"])
            def repeat_all_messages(message: Message): # Название функции не играет никакой роли
                ADMIN_ID = message.from_user.id
                config_content = config_template.format(TOKEN=TOKEN, ADMIN_ID=ADMIN_ID)
                f = open('config.py', 'w', encoding='utf-8')
                f.write(config_content)
                f.close()
                bot.send_message(message.chat.id, 'Конфиг обновлён')
                print('Конфиг обновлён')

                import config
                if os.path.exists(config.DB_WORK):
                    os.remove(config.DB_WORK)
                if os.path.exists(config.DB_STATES):
                    os.remove(config.DB_STATES)

                conn = sqlite3.connect(config.DB_WORK)
                f_sql = open(config.DB_WORK[:-2] + 'sql', encoding='utf-8')
                conn.executescript(f_sql.read())
                f_sql.close()
                conn.close()

                adminer = AdminWorker()
                adminer.add(message.from_user)
                adminer.close()

                bot.send_message(message.chat.id, 'Вы добавлены в базу как админ')
                print('Вы добавлены в базу как админ')


            bot_inf = bot.get_me() 
            print(f'Отправь мне что-то https://t.me/{bot_inf.username}')
            bot.infinity_polling()
