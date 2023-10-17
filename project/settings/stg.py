"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 4.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from .base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-a=&^z@quui-wci&n086wd$yz6b9u_t#9-u$$nd%kdd4kpbf&s-'

ALLOWED_HOSTS = ['*']
STATIC_ROOT =  '/var/www/html/magdig/static'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mitsdb',
        'USER': 'web_magdig',
        'PASSWORD': 'mits-P@web_magdig1!',
        'HOST': 'magcraft-stg-db-instance-1.cz2pm4xengae.ap-northeast-1.rds.amazonaws.com',
        'PORT': '5432',
    },
}

# Google Analytics 本番：G-LF094FFW3E、STG：G-D4X2X5RZL9
GA_GTAG_CODE ='G-D4X2X5RZL9'

# Login_User Logs
LOGS_PATH = '/usr/mag_sys/logs/magdig/'
