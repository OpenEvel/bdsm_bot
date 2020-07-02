# -*- coding: utf-8 -*-
from bot import bot
import config
from .dber import Admin, AdminWorker


@bot.message_handler(commands=["1"])
def cmd(message):
    bot.send_message(message.chat.id, 'Пидр')
