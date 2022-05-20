# YAMDB

Обзоры и мнения о медиа.


![Action status](https://github.com/Nastasia153/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)


## Установка

Клонируйте репозиторий.

## Использование

Наполнение .env файла

в директории infra, есть шаблон заполнения .env файла.
### Запуск docker-compose 

```
sudo docker-compose up -d --build
```
- выполняем миграции:
```
sudo docker-compose exec web python manage.py migrate
```
- создаём суперпользователя:
```
sudo docker-compose exec web python manage.py createsuperuser
```
- собираем статику:
```
sudo docker-compose exec web python manage.py collectstatic --no-input
```

Теперь проект доступен по адресу [http://localhost/api/v1/titles/](http://localhost/api/v1/titles)


После запуска локального сервера документация API доступна по адресу [http://localhost/redoc/](http://localhost/redoc/)

## Технологии

Приложение работает на 
- [Django 2.2](https://www.djangoproject.com/download/)
- [Django REST Framework 3.12](https://www.django-rest-framework.org/#installation).
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/).
- [Docker](https://docs.docker.com/)
- [GitHub Actions](https://github.com/features/actions)


## Разработчики

Проект разработан
- [Анастасия Дементьева](https://github.com/Nastasia153)
- [Александр Рубцов](https://github.com/FinemechanicPub)
- [Виталий Насретдинов](https://github.com/nasretdinovs)


## License
[MIT](https://choosealicense.com/licenses/mit/)