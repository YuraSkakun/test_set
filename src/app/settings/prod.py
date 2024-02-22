from app.settings.components.base import * # noqa

from app.settings.components.database import * # noqa

from app.settings.components.email import * # noqa

import os

SECRET_KEY = os.environ['SECRET_KEY']

# CSRF_TRUSTED_ORIGINS=['http://ec2-3-70-177-79.eu-central-1.compute.amazonaws.com',
#                       'http://3.70.177.79',
#                       'http://127.0.0.1',
# ]


ALLOWED_HOSTS = ['*', '127.0.0.1', 'localhost']
# ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
# ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(':')

DEBUG = False

# STATIC_ROOT = os.path.join(BASE_DIR, 'cdn/static')
STATIC_ROOT = '/var/www/tmb/static'

# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_ROOT = '/var/www/tmb/media'

# CELERY_BROKER_URL = 'amqp://rabbitmq'

print('')


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         # 'NAME': 'prod',
#         # 'HOST': '10.30.0.5',
#         # 'USER': 'admin-prod',
#         # 'PASS': 'passw-prod',
#         'NAME': os.environ['NAME'],
#         'HOST': os.environ['HOST'],
#         'USER': os.environ['USER'],
#         'PASS': os.environ['PASS'],
#     }
# }
