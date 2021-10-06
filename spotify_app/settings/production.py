import os
from .base import *


# TODO: Define the root address of the project in production later
PRODUCTION_HOST = os.environ.get('PRODUCTION_HOST')
HOST_ROOT = os.environ.get('HOST_ROOT')

SECURE_HSTS_SECONDS = 60
SESSION_COOKIE_SECURE = True
SECURE_REFERRER_POLICY = 'same-origin'
SECRET_KEY = os.environ.get('BACKEND_SECRET_KEY')
DEBUG = False
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

ALLOWED_HOSTS = [
    PRODUCTION_HOST,
]

CSRF_COOKIE_SECURE = True
