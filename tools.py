# -*- coding: utf-8 -*-
import os
from importlib import import_module

def load_handlers(module_name, module_bot='bot'):
    """
    Функция возвращает переменную "module_bot" telegram бота
    из модуля "module_name", где находятся обработчики для этого бота.
    Таким хитрым способом можно хранить обработчики бота в разных модулях
    и загружать их в главном приложении при помощи этой функции.
    В разных модулях функции-обработчики могут называтся одинаково
    """
    module = import_module(module_name)
    bot = getattr(module, module_bot, None)
    if not bot:
        raise AttributeError(f"Переменной бота '{module_bot}' НЕТ в модуле {module_name}")
    return bot
