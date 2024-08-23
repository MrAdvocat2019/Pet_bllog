A pet blog project on django with celery

For launch run: `cd blog` then

1. Create postgres database called blog, username и password you can change in settings.py
2. Create and activate venv
3. In terminal execute server will be running on localhost 8080
    ``` 
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
    ```
4. In separate terminal without active venv run `redis-server`
5. In third terminal with activated venv run `celery -A blog worker -l info` 

You launched the project! But don't use this for production, this server is not suitable for that!!!!

Alternitavely you can change
```PYTHON
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
```
to
```PYTHON
CELERY_BROKER_URL = 'redis://redis:6379'
CELERY_RESULT_BACKEND = 'redis://redis:6379'
```
and 
```
'HOST': 'localhost',
```
in settings.DATABASE to
```
'HOST': 'pgdb',
```
and run `docker-compose up` from the root directory(not the blog)
