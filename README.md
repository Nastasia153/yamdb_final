# YAMDB

Обзоры и мнения о медиа.

## Установка

Клонируйте репозиторий.

## Использование

Наполнение .env файла
```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
```
### Запуск docker-compose 

```
docker-compose up -d --build
```
- выполняем миграции:
```
docker-compose exec web python manage.py migrate
```
- создаём суперпользователя:
```
docker-compose exec web python manage.py createsuperuser
```
- собираем статику:
```
docker-compose exec web python manage.py collectstatic --no-input
```

Теперь проект доступен по адресу [http://localhost/api/v1/titles/](http://localhost/api/v1/titles)


После запуска локального сервера документация API доступна по адресу [http://localhost/redoc/](http://localhost/redoc/)

## Технологии

Приложение работает на 
- [Django 2.2](https://www.djangoproject.com/download/)
- [Django REST Framework 3.12](https://www.django-rest-framework.org/#installation).
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/).
- [Docker](https://docs.docker.com/)

## Разработчики

Проект разработан 
- [Александр Рубцов](https://github.com/FinemechanicPub)
- [Анастасия Дементьева](https://github.com/Nastasia153)
- [Виталий Насретдинов](https://github.com/nasretdinovs)


## License
[MIT](https://choosealicense.com/licenses/mit/)