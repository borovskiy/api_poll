
Установка:
Склонируйте репозиторий
Создайте и войдите в вирутальное окружение
Установите зависимости:
pip install -r requirements.txt
Проведите миграции
python manage.py makemigrations
python manage.py migrate
Создайте суперпользователя
python manage.py createsuperuser
Запустите тестовый сервер
python manage.py runserver
Остановите тестовый сервер
Выполните команду
python manage.py add_bd
Запустите тестовый сервер
python manage.py runserver

Документация по API
Алгоритм авторизации пользователей
Пользователь отправляет запрос с параметрами username и password на /api-token-auth/, 
в ответе на запрос ему приходит token (JWT-токен) в поле access.
При отправке запроса передавайте токен в заголовке Authorization: Token <токен>

Добавление/Изменение/Удаление опросов (POST)
Права доступа: Администратор
URL: /api/polls/
QUERY PARAMETERS: title, start_date, end_date,description
URL: /api/polls/<poll_id>/
QUERY PARAMETERS: title, end_date,description

Получение списка активных опросов (GET)
Права доступа: Любой пользователь
URL: /api/polls/
Получение списка всех опросов (GET)
Права доступа: Администратор
URL: /api/polls/
URL: /api/polls/<poll_id>/


Добавление/Изменение/Удаление вопросов к опросу (POST)
Права доступа: Администратор
URL: /api/polls/<poll_id>/questions/
URL: /api/polls/<poll_id>/questions/<question_id>/
QUERY PARAMETERS: text, type_question (text_field--radio--check_boxes)

Получение списка активных вопросов к опросу (GET)
Права доступа: Любой пользователь
URL: /api/polls/

Получение списка всех вопросов к опросу (GET)
Права доступа: Администратор
URL: /api/polls/<poll_id>/questions/
URL: /api/polls/<poll_id>/questions/<question_id>/


Добавление и просмотр вариантов ответа к вопросу (POST)
Права доступа: Администратор
URL: /api/polls/<poll_id>/questions/<question_id>/response/
QUERY PARAMETERS: text



Прохождение опроса (POST)
Права доступа: Авторизованный пользователь или или неавторизованный пользователь который передал id_user
URL: /api/polls/<poll_id>/questions/<question_id>/answer/
QUERY PARAMETERS:'self_response' or 'one_response' or 'many_response' в зависимости от типа ответа передается id ответа(список id выкатывается в GET  запросе)

Получение пройденных пользователем опросов (GET)
Права доступа: Администратор
URL: /api/user/
URL: /api/user/<id>