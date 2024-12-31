"""
Django settings for school project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
import dj_database_url 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-gs@6%!(at0d$a*&^_%2dvu4=#9d3o2gk*$d-hjpr*3=#0%8d@i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['school-htaf.onrender.com', 'localhost', '127.0.0.1']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'playground', 
    'captcha', 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware', 
    'django.middleware.common.XForwardedHostMiddleware',  # Ajout de ce middleware
]

ROOT_URLCONF = 'school.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [os.path.join(BASE_DIR, 'playground', 'templates')],
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

WSGI_APPLICATION = 'school.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }}
 
   
# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators
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


# https://docs.djangoproject.com/en/5.1/topics/i18n/

# Langue par défaut
LANGUAGE_CODE = 'fr'
# Activer la détection de la langue via middleware


TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# URL pour accéder aux fichiers statiques
STATIC_URL = '/static/'

# Chemin racine où les fichiers statiques collectés iront (en production)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Répertoires additionnels contenant des fichiers statiques
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # Assure-toi que le dossier 'static' est au bon endroit
]
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True  
EMAIL_HOST_PASSWORD = 'esae robb anrm oqmv' 
EMAIL_HOST_USER ='ali0braiki0@gmail.com' 

  
#RECAPTCHA_PUBLIC_KEY = '6LfrKJEqAAAAAJcC5rRbpuHKyW_uqEHwO0nYCO41'
#RECAPTCHA_PRIVATE_KEY = '6LfrKJEqAAAAAC48iR1FXCN5ZqKUTrN0mu6Abj0A'
#SILENCED_SYSTEM_CHECKS = ['captcha.reCAPTCHA_TEST_MODE']


