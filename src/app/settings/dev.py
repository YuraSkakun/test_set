from app.settings.components.base import * # noqa
# from app.settings.components.database import * # noqa
from app.settings.components.dev_tools import * # noqa
from app.settings.components.database import * # noqa
from app.settings.components.email import * # noqa

DEBUG = True

ALLOWED_HOSTS = ['*', '127.0.0.1', 'localhost']
# ALLOWED_HOSTS = ['*']

STATIC_ROOT = os.path.join(BASE_DIR, 'cdn/static')

# CELERY_BROKER_URL = 'redis://localhost:6379'

# CELERY_BROKER_URL = 'amqp://localhost'
CELERY_BROKER_URL = 'amqp://rabbitmq'  # docker-compose

# from celery.schedules import crontab

# CELERY_BEAT_SCHEDULE = {
#     'parse': {
#         'task': 'testsuite.tasks.cleanup_outdated_testruns',
#         'schedule': crontab(minute='*/1'),
#     },
# }

# print('')
