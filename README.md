# Приложение «Продуктовый помощник»
### Описание
Приложение «Продуктовый помощник» - сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

### Шаблон наполнения env-файла
```
SECRET_KEY=p&l%385
DEBUG = False
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=11111
DB_HOST=db
DB_PORT=5432
```
### Запуск приложения в контейнерах
- склонируйте репозиторий
- зайдите в папку  foodgram-project-react/infra и выполните команду(если Linux - любую команду начинайте с sudo): 
``` docker-compose up ```
Проект запущен и доступен по адресу http://localhost/.


Для остановки контейнеров выполните:
``` docker-compose stop ```

### Примеры запросов к API: 
``` 
GET: 
http://localhost/api/users/ 
{
    "count": 123,
    "next": "http://foodgram.example.org/api/users/?page=4",
    "previous": "http://foodgram.example.org/api/users/?page=2",
    "results": [
        {
            "email": "user@example.com",
            "id": 0,
            "username": "string",
            "first_name": "Вася",
            "last_name": "Пупкин",
            "is_subscribed": false
        }
    ]
}

POST: 
http://localhost/api/v1/recipes/ 
request example:
{
    "ingredients": [
        {
            "id": 1123,
            "amount": 10
        }
    ],
    "tags": [1,2],
    "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
    "name": "string",
    "text": "string",
    "cooking_time": 1
}

response example:
{
    "id": 0,
    "tags": [
        {
            "id": 0,
            "name": "Завтрак",
            "color": "#E26C2D",
            "slug": "breakfast"
        }
    ],
    "author": {
        "email": "user@example.com",
        "id": 0,
        "username": "string",
        "first_name": "Вася",
        "last_name": "Пупкин",
        "is_subscribed": false
    },
    "ingredients": [
        {
            "id": 0,
            "name": "Картофель отварной",
            "measurement_unit": "г",
            "amount": 1
        }
    ],
    "is_favorited": true,
    "is_in_shopping_cart": true,
    "name": "string",
    "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
    "text": "string",
    "cooking_time": 1
}
``` 
### Автор
Клементьева Евгения

Сервер: 158.160.4.38
Администрирование: 
    логин - admin
    пароль - 12345

![foodgram_workflow](https://github.com/KlementevaE/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
