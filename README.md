# GradSchoolZero
The application is a graduate program management system that can be used by Registrars, Instructors, students and visitors in the Graduate School.

`Phase I report:'
`
https://docs.google.com/document/d/1DAu1bj3FWoDtEsOTPkQOJbSO8nXbTuFDSy1ARNMdvVw/edit?usp=sharing


`Phase II report:` https://docs.google.com/document/d/1yz6FoeKtJqNopBGAmZwHEI0rfkARW_sjMqGpyztAHmI/edit?usp=sharing

`Instructions to run the project`

1. First create django environment to the local machine

python3 -m venv env

2. Activate the environment

source env/bin/activate

3. Install the following libraries(one at a time). Also mentioned in the requirements.txt file

pip install django
pip install pillow
pip install celery
pip install django-crispy-forms
pip install django-tinymce

4. Make migrations

python manage.py makemigrations

5. Migrate

python manage.py migrate

6. Finally runserver which will provide the link to the web

python manage.py runserver




