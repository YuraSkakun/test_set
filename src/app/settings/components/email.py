# from app.settings.components.base import *

import os

# EMAIL_HOST = os.environ['EMAIL_HOST']
# EMAIL_PORT = os.environ['EMAIL_PORT']
# EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
# EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
