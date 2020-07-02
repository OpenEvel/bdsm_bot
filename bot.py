# -*- coding: utf-8 -*-
import telebot
import config
import tools

bot = telebot.TeleBot(config.TOKEN)

if __name__ == "__main__":
    # загружаем обработчики для бота
    bot = tools.load_handlers("logic.admins.handlers")
    bot.send_message(config.ADMIN_ID, 'Бот запущен')
    # начинам обрабатывать сообщения от пользователей
    bot.infinity_polling()