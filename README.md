# backend

#### Веб-сервер, для обработки и хранения информации о пользователях и их операциях
#
Стек технологий:
- Django, DRF, Channels
- Celery
- Celery Beat
- Postgresql
- Swagger

## Сборка из исходного кода
#### Установка зависимостей
```shell
$ python3 -m venv venv
$ source venv/bin/activate
$ cd app
$ pip install -r reuirements/base.txt
$ mv .env.example .env
```

#### Подготовка бд
```shell
$ python3 manage.py makemigrations && python3 manage.py migrate users
$ python3 manage.py migrate
$ python manage.py loaddata departmens.json 
```

#### Запуск веб сервера
```shell
$ python3 manage.py runserver
```

#### Запуск celery
```shell
$ celery -A conf worker --loglevel=INFO
```
