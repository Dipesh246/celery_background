import os
from celery import Celery
#set the default django settings to celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backgroundtest.settings')
app = Celery('backgroundtest')
app.config_from_object('django.conf:settings', namespace='CELERY')
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
#message broker configurations
BASE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
app.conf.broker_url = BASE_REDIS_URL
#creating a celery beat scheduler to start the tasks
app.conf.beat_scheduler = 'django_celery_beat.schedulers.DatabaseScheduler'

app.conf.beat_schedule = {
    'add-every-3-seconds': {
        'task': 'tasks.add',
        'schedule': 3.0,
        'args': (16, 16)
    },
}
app.conf.timezone = 'UTC'