# -*- coding: utf-8 -*-
import os
import sys
import sqlite3
import telebot

# Делаем видимыми модули уровнем
module_dir = os.path.split(os.path.abspath(__file__))[0]
workspace_dir = os.path.normpath(os.path.join(module_dir, os.pardir))
sys.path.append(workspace_dir)

from logic.admins.tabler import AdminsWorker

if __name__ == "__main__":
    args = sys.argv[1:]
    TOKEN = args[0]

    bot = telebot.TeleBot(TOKEN)

    @bot.message_handler(content_types=["text"])
    def repeat_all_messages(message): # Название функции не играет никакой роли
        ADMIN_ID = message.from_user.id
        # config_content = config_template.format(TOKEN=TOKEN, ADMIN_ID=ADMIN_ID)
        f_r = open(os.path.join(workspace_dir, 'config.py'), 'r', encoding='utf-8')
        config_content = ""
        for line in f_r:
            if line.startswith("TOKEN ="):
                line = f"TOKEN = '{TOKEN}'\n"
            if line.startswith("ADMIN_ID ="):
                line = f"ADMIN_ID = {ADMIN_ID}\n"
            config_content += line
        f_r.close()

        f_w = open(os.path.join(workspace_dir, 'config.py'), 'w', encoding='utf-8')
        f_w.write(config_content)
        f_w.close()
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

        adminer = AdminsWorker()
        adminer.add(message.from_user)
        adminer.close()

        bot.send_message(message.chat.id, 'Вы добавлены в базу как админ')
        print('Вы добавлены в базу как админ')
        bot.stop_polling()
        os._exit(0)        # Быстрохак - никак не получается выключить бота


    bot_inf = bot.get_me()
    print(f'Отправь мне что-нибудь https://t.me/{bot_inf.username}')
    bot.polling(none_stop=False)
