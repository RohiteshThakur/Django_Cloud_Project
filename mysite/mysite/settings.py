"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 2.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from django.urls import reverse_lazy


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)  # below snippet returns: /media/redhat/apps/Django_project/mysite
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '<secret_key>'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudify',
    'django.contrib.admin',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',                           # Added by me for serving static files.
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mysitedb',
        'USER': 'dbadmin',
        'PASSWORD': 'dbadmin',
        'HOST': 'localhost',
        'PORT': '',

    },

    'ratecarddb': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ratecarddb',
        'USER': 'dbadmin',
        'PASSWORD': 'dbadmin',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

# URL Prefix for static files. What are we going to tag along web address? e.g. "http://127.0.0.1/static/"
STATIC_URL = '/static/'


# Note on STATIC_ROOT: Absolute path of the directory where static files should be collected "to". 
# ----> DON'T PUT ANYTHING IN THIS DIRECTORY: Store your static files in App's static/ subdirectories and in STATICFILES_DIRS <----
# e.g. '/home/redhat/staticfiles/'
# THIS IS THE FOLDER WHERE FILES FROM "STATICFILES_DIRS" will be copied to after: #python manage.py collectstatic
STATIC_ROOT = os.path.join(BASE_DIR, 'cloudify/static')             # Note the missing "/" before cloudify.


# Additional location of static files. WE KEEP THE STATIC FILES HERE.
STATICFILES_DIRS = (
    # Put strings like "/home/redhat/staticfiles/assets/"
    # Always use "/" even on windows.
    # Always use absolute path and not relative path.
    os.path.join(os.path.dirname(BASE_DIR), "static"),
    )


DATABASE_ROUTERS = ['cloudify.router.CloudifyRouter']

ALLOWED_HOSTS = ['localhost', '127.0.0.1']              # To be change when deployed to production.


TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),                # Added by me for linkining templates. My BASE_DIR: /media/redhat/apps/Django_project/mysite
)

# Parameters used in Django Authentication. These variables were defined after configuring USER authentication using Django built-ins.
LOGIN_REDIRECT_URL = reverse_lazy('home')               # 'reverse_lazy' builds URLs by their names e.g. builds 'frontend/landing-page' from 'home'
LOGIN_URL = reverse_lazy('login')
LOGOUT_URL = reverse_lazy('logout')

# http://test-driven-django-development.readthedocs.io/en/latest/03-views.html