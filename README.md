# _bdsm_bot_
#### Это крутой телеграм бот для управления проектами, который может работать как в Windows так и в Linux

<a href="url"><img src="https://user-images.githubusercontent.com/37779327/87092364-f52a2a00-c243-11ea-90c5-b5609cfa02ae.jpg" align="left" height="60" width="60" ></a>
Если ты крутой разарб,  
то заходи на нашу [wiki](https://github.com/OpenEvel/bdsm_bot/wiki)

---
## Настройка проекта для работыы

НИИ8 был разработан специальный скрипт **pdm.py** (project deploy manager), который призван облегчить жизнь программисту.

Так как есть некоторые различия между операционными системами, то для удобства дальше под __*py*__  
будет пониматься **интерпретатор** __*python*__, который установлен в вашей системе
* **_В Windows это_**: `py` или `python`
* **_В *nix подобных системах лучше всегда писать_** `python3`

### __1. Виртуальное окружение:__
Чтобы создать виртуальное окружение и установить в него все нужные библиотеки в папке проекта (bdsm_bot) выполните:
  ```console
  py -m pdm --install
  ```
### __2. Персональные настройки:__
Работает если вы выполнили пункт 1.  
Врядли будет удобно работать нескольким программистам с одним ботом на всех. Для тестов и разработки лучше иметь отдельных ботов,
после настройки которых локальный проект превратиться в обособленный, независящий от других.  
Чтобы настроить бота нужно: 

1. Прописать в **_config.py_**:
    * Токен бота
    * ID админа (разработчика)
2. Создать базу данных и добавить туда разработчика как админа
3. Сделать **_config.py_** невидимым для git, чтобы случайно не запушить на сервер персональные настроки, что просто не безопасно

Все эти пункты выполняет:
  ```console
  py -m pdm --config YOUR_TOKEN
  ```
Если вы например забыли ввести токен, то вам будет предложено ввести его,  
то есть комманда `py -m pdm --config` - **коректна**  
Кстати, строка токена может быть указана:
* без кавычек - YOUR_TOKEN
* в кавычках -  "YOUR_TOKEN" или 'YOUR_TOKEN'
* по ошибке содержать кавычки в любом месте:
    * "YOUR_TOKEN
    * YOU"R_TOKEN
    * YOUR_TOKEN"
И во всех случаях **pdm.py** правильно извлечёт строку токена.

Если вы случайно испортили **_config.py_**, то комманда ниже загружает старую версию **_config.py_** с сервера (ветка master):
  ```console
  py -m pdm --config reset
  ```
Если вам нужно внести изменения в **_config.py_** и запушить их на сервер, то комманда ниже делает этот файл видимым для git
  ```console
  py -m pdm --config visible
  ```
### __3. Настройка IDE:__
Если вы работаете в **Visual Studio Code**, то все нужные настроки для него можно установить при помощи комманды:
  ```console
  py -m pdm -v
  ```
Если вы работает в **PyCharm** то нужно в настройках указать виртуальное окружение, где установлены нужные бибилиотеки:

**Заходим в настройки**  
![image](https://user-images.githubusercontent.com/37779327/87087402-b09a9080-c23b-11ea-81a5-646e36c48d76.png)

**Ищем интерпретатор из виртуального окружения**  
Он расположен в зависимости от платформы внутри где-то (bdsm_bot/venv/.../python)  
Или нам Pycharm сразу найдёт его  
![image](https://user-images.githubusercontent.com/37779327/87087654-2bfc4200-c23c-11ea-9479-e07d670fa8ed.png)

Не забываем нажать `ОК` или `Apply`  
![image](https://user-images.githubusercontent.com/37779327/87088175-fdcb3200-c23c-11ea-9a8f-9b027116ad35.png)

### __4. Запуск бота__
Различается от IDE, главное помнить, что нужно запускать файл **bot.py**

# Дополнительно
Пункты 1-3 можно объединить в одну комманду:  
Создать виртуальное окружение и настроить бота и его **_config.py_**
```console
py -m pdm --install --config YOUR_TOKEN
```
Причём порядок следования аргументов не имеет значения. Можно писать как хочешь
```console
py -m pdm --config --install YOUR_TOKEN
```
```console
py -m pdm --config YOUR_TOKEN --install
```
```console
py -m pdm YOUR_TOKEN --config --install
```

Или в комманде просто не указывать токен, его потом предложат ввести
```console
py -m pdm --config --install
```
```console
py -m pdm --install --config
```

---

# Структура проекта
* ## bot.py
    Главная прграмма - запускает наш телеграм бот
* ## config.py
    Конфигурационный файл - содержит токен бота, id админа и путь до базы данных

