from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Django will always save session information to the database for every request
SESSION_SAVE_EVERY_REQUEST = True

HOST_ROOT = "http://localhost:5000"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1"
]

# Secret key uniquely used in degub. Please use a secure key for production
SECRET_KEY = 'kg+!1c&ez!6k-ewilbh&_1mt0nyl91%dbuecdmpf2fy)je*(6g'
