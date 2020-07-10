# -*- coding: utf-8 -*-
import os
import sys
import time
import subprocess
import json
import shutil
from urllib.request import urlopen

def is_win():
    return 'win' in sys.platform

def status_bar(title:str=None, *, command:str, ts:float=0.25):
    """
        title   : сообщение пользователю (что будет выводиться вместо самой комманды)
        command : комманда оболочки (что выполняется)
        ts      : интервал времени между анимацией статус бара
    """
    ENCODING_CONSOLE = 'cp1251' if is_win() else 'utf8'

    if not title:
        title = command

    write, flush = sys.stdout.write, sys.stdout.flush
    animations = ['|', '/', '-', '\\' ]  # Элементы анимации статус бара

    # Запускаем комманду command через subprocess
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    i_a = -1
    while True:
        if process.poll() is not None:
            # При работе программы были ошибки
            if process.poll() != 0:                
                if process.stderr:
                    write(f'\r\t{title}: [NO]\n')
                    write(f'command: {command}\n')
                    write('-----------------------ERROR MESSAGE---------------------\n')
                    flush()
                    while True:
                        err = process.stderr.readline()
                        err = err.decode(ENCODING_CONSOLE)

                        if err == '':
                            write('---------------------------------------------------------\n')
                            flush()
                            # Выходим из цикла вывода ошибок
                            break
                        if err != '':
                            write(f'{err}')
                            flush()
            else:
                # Прграмма завершилась нормально
                write(f'\r\t{title}: [OK]\n')
                flush()

            # Выхлодим из бесконечного цикла анимации
            break

        # Получаем индекс анимации (не выходящий за пределы массива анимаций)
        # По сути проходим по списку анимаций круг за кругом
        i_a = (i_a + 1) % len(animations)

        # Обновляем анимацию в статус баре (благодаря символу возврата каретки '\r')
        write(f'\r\t{title}: [{animations[i_a]}]')
        flush()

        # Делаем перерыв между анимациями, чтобы не получилась каша
        time.sleep(ts)

if __name__ == "__main__":
    # Переменные командной строки
    # Представляет собой список всех слов, что идут после pdm
    # в командве: python -m pdm --config --venv -vscode и тд
    args = sys.argv[1:]

    # Установить виртуальное окружение со всеми библиотеками
    if '--venv' in args:
        # Системный интерпретатор python
        python_global_exe = "python" if is_win() else 'python3'
        # Создаём виртуальное окружение
        status_bar("making 'venv' directory", command=f"{python_global_exe} -m venv venv")

        # pip из виртуального окружения
        pip_exe = ".\\venv\\Scripts\\pip" if is_win() else "./venv/bin/pip"
        # Обновляем pip
        status_bar("upgrading pip", command=f"{pip_exe} install --upgrade pip --user")

        # Устанавливаем нужные для работы бота библиотеки
        print("\tpip installing requirements(python libraries):")
        for lib in open('set_env/requirements.txt', 'r', encoding='utf8'):
            # Очищаем строку с названием бмблиотеки от пробельных символов
            lib = lib.strip()
            # Статус бар для каждой отдельной библиотеки
            status_bar(f"\t{lib}", command=f"{pip_exe} install {lib}")            
    
    # Установить настройки для vscode
    if '-vscode' in args:
        path_settings = os.path.normpath("./set_env/vscode/settings.json")
        with open(path_settings, "r", encoding='utf8') as read_file:
            settings = json.load(read_file)
        
        pythonPath = '.\\venv\\Scripts\\python' if is_win() else "./venv/bin/python"
        settings['python.pythonPath'] = pythonPath

        if not os.path.exists(".vscode"):
            os.mkdir('.vscode')

        with open(os.path.normpath(".vscode/settings.json"), "w", encoding='utf8') as write_file:
            json.dump(settings, write_file)
        
        shutil.copy(os.path.normpath("./set_env/vscode/launch.json"), os.path.normpath(".vscode/launch.json"))

    # Всякие действия с файлом config.py
    if '--config' in args:
        # Сделать config.py ВИДИМЫМ для git - чтобы запушить изменения в нём
        if 'visible' in args:
            os.system("git update-index --no-assume-unchanged config.py")
        # Восстановить старую копию файла config.py
        elif 'reset' in args:
            #делаем запрос на файл конфига
            send = urlopen('https://github.com/OpenEvel/bdsm_bot/raw/master/config.py')
            config_content = send.read().decode('utf8')
            # Открываем файл на запись
            with open('config.py', 'w', encoding='utf8') as conf_file:
                conf_file.write(config_content)
        # Настроить config.py для запуска бота
        else:
            # Делаем config.py НЕвидимым для git
            os.system("git update-index --assume-unchanged config.py")

            # Получаем токен от пользователя
            # Токен могли ввести в одной строке со всеми коммандам
            # Удаляем все возможные комманды, что мог ввести пользователь
            args.remove('--config')
            if '--venv' in args:
                args.remove("--venv")
            if '-vscode' in args:
                args.remove("-vscode")

            # Если список комманд НЕ пустой            
            if args:
                # То в списке комманд остался только токен
                TOKEN = args[0]
            else:
                # Пользователь не ввёл токен
                # Пропросим пользователя ввести токен
                TOKEN = input("Введите токен: ")
            # В строке токина могут содержаться лишние символы
            TOKEN = TOKEN.strip()
            # Кто-то по ошибке мог вставить в строку токена кавычки
            # Уберём их
            trash = ["\'", "\""]
            for bad in trash:
                TOKEN = TOKEN.replace(bad, '')

            # Устанавливаем файл настроек для работы бота
            if is_win():
                os.system(f'.\\venv\\Scripts\\python .\\set_env\\install_config.py {TOKEN}')
            else:
                os.system(f'./venv/bin/python ./set_env/install_config.py {TOKEN}')
