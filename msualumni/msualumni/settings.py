"""
Django settings for msualumni project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(__file__)

PROJECT_PATH = os.path.abspath(os.path.join(BASE_DIR, os.pardir))

TEMPLATE_PATH = os.path.join(PROJECT_PATH, 'templates').replace('\\', '/')

STATIC_PATH = os.path.join(PROJECT_PATH, 'static').replace('\\', '/')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['KEYSTONE']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.webdesign',
    'bootstrap3',
    'south',
    'profiles',
    'alumniadmin',
    'news'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'msualumni.urls'

WSGI_APPLICATION = 'msualumni.wsgi.application'

import dj_database_url
# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {}
DATABASES['default'] = dj_database_url.config(env='ALUMNI_DB_URL')

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'NAME': 'alumni_db',
#        'HOST': '127.0.0.1',
#        'PORT': '5432',
#        'PASSWORD': 'admin',
#        'USER': 'postgres'
#    }
#}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = 'staticfiles'

STATIC_URL = '/static/'

STATICFILES_DIRS = (STATIC_PATH,)

TEMPLATE_DIRS = (TEMPLATE_PATH,)

MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media').replace('\\', '/')

MEDIA_URL = '/media/'

AUTH_USER_MODEL = 'alumniadmin.User'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
LOGIN_REDIRECT_URL = '/admin/dashboard'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'jerico.delfinado@gmail.com'
EMAIL_HOST_PASSWORD = 'upward123'








