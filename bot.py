# -*- coding: utf-8 -*-
import telebot
import config
import utils

bot = telebot.TeleBot(config.TOKEN)

if __name__ == "__main__":
    # загружаем обработчики для бота
    bot = utils.tools.load_handlers("utils.admins.handlers")
    bot.send_message(config.ADMIN_ID, 'Бот запущен')
    # начинам обрабатывать сообщения от пользователей
    bot.infinity_polling()