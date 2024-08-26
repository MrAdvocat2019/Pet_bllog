A pet blog project on django with celery


0. in .env.template put your telegram api key and a link on your bot(full link with https and etc) and then execute `cp .env.template .env` then `cd blog`
1. Create postgres database called blog, username и password you can see and change in settings.py
2. Create and activate venv
3. In terminal execute server will be running on localhost 8000
   ```
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver
   ```
4. In separate terminal run `python manage.py run_bot`

5. In separate terminal without active venv run `redis-server`
6. In third terminal with activated venv run `celery -A blog worker -l info`

You launched the project! But don't use this for production, this server is not suitable for that!!!!

Alternitavely you can use docker but dont even try
