from app.settings.base import * # noqa

import os

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['*']

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         # 'NAME': 'prod',
#         # 'HOST': '10.30.0.5',
#         # 'USER': 'admin-prod',
#         # 'PASS': 'passw-prod',
#         'NAME': os.environ['DB_NAME'],
#         'HOST': os.environ['DB_HOST'],
#         'USER': os.environ['DB_USER'],
#         'PASSWORD': os.environ['DB_PASS'],
#     }
# }
