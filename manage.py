# -*- coding: utf-8 -*-
import os
import sys
import time
import subprocess

def is_win():
    return 'win' in sys.platform

ENCODING_CONSOLE = 'cp1251' if is_win() else 'utf8'

def status_bar(title:str=None, *, command:str, ts:float=0.25):
    """
        title   : сообщение пользователю (что будет выводиться вместо самой комманды)
        command : комманда оболочки (что выполняется)
        ts      : интервал времени между анимацией статус бара
    """
    if not title:
        title = command

    # На всякий случай очищаем title от лишних пробелов(для красоты форматирования)
    title = title.strip()

    write, flush = sys.stdout.write, sys.stdout.flush
    animations = ['|', '/', '-', '\\' ]  # Элементы анимации статус бара

    # Запускаем комманду command через subprocess
    process = subprocess.Popen(command,  stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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
    args = sys.argv[1:]

    if '--install' in args:
        if is_win():
            status_bar("making 'venv' directory", command="python -m venv venv")
            status_bar("upgrading pip", command='.\\venv\\Scripts\\pip install --upgrade pip --user')
            status_bar("pip installing requirements(python libraries)", command=".\\venv\\Scripts\\pip install -r .\\set_env\\requirements.txt")

    if '--config' in args:
        if 'visible' in args:
            os.system("git update-index --no-assume-unchanged config.py")
        else:
            # Делаем config.py невидимым для git
            os.system("git update-index --assume-unchanged config.py")

            # Получаем токен от пользователя
            args.remove('--config')
            if '--install' in args:
                args.remove("--install")
            if args:
                TOKEN = args[0]
            else:
                TOKEN = input("Введите токен: ")
            # В строке токина могут содержаться лишние символы
            TOKEN = TOKEN.strip()
            # Кто-то по ошибке мог вставить в строку токин кавычки
            trash = ["\'", "\""]
            for bad in trash:
                TOKEN = TOKEN.replace(bad, '')
            
            # Устанавливаем файл настроек для работы бота
            if is_win():
                os.system(f'.\\venv\\Scripts\\python .\\set_env\\install_config.py {TOKEN}')
