# coding=utf-8
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': os.getenv("POSTGRES_HOST", "oj-postgres"),
        'PORT': os.getenv("POSTGRES_PORT", "5432"),
        'NAME': os.getenv("POSTGRES_DB"),
        'USER': os.getenv("POSTGRES_USER"),
        'PASSWORD': os.getenv("POSTGRES_PASSWORD")
    }
}

REDIS_CONF = {
    "host": os.getenv("REDIS_HOST", "oj-redis"),
    "port": os.getenv("REDIS_PORT", "6379")
}

DEBUG = False

DATA_DIR = os.path.join(BASE_DIR, 'data')
