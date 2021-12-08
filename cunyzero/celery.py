import os
from django.conf import settings
from celery import Celery
from celery.schedules import crontab
from django.db.models.aggregates import Count
from course.tasks import handle_semester_stage


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cunyzero.settings')

app = Celery('cunyzero')

app.conf.timezone = 'UTC'


# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, trigger_semester_stage, name='trigger_semester_stage')

app.conf.beat_schedule = {
    'update-semester-every-30-seconds': {
        'task': 'cunyzero.celery.trigger_semester_stage',
        'schedule': 10.0,
    },
}

@app.task
def trigger_semester_stage():
    handle_semester_stage()

if __name__ == '__main__':
    app.start()