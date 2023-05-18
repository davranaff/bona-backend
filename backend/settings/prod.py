from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'bonafresco79db',
        'USER': 'super',
        'PASSWORD': '4:jHGbE_2v:sHfZ',
        'HOST': 'BonaFresco79-2659.postgres.pythonanywhere-services.com',
        'PORT': 12659
    }
}

ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOWED_ORIGINS = ['https://localhost:3000']
