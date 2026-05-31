from decouple import config
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')


# if you costomize the page_404 look this link : https://www.w3schools.com/django/django_404.php
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Store',
    'acounts',
    'cart',
    'orders',
    'coupons',
    'crispy_forms',
    'crispy_bootstrap5',
    'django.contrib.postgres',
]

# CONECTING CRISPY WITH BOOTSTRAP5
CRISPY_TEMPLATE_PACK = 'bootstrap5'


# Custom user model
AUTH_USER_MODEL = 'acounts.Acount'
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]




MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecom.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processore.cart'
            ],
        },
    },
]

WSGI_APPLICATION = 'ecom.wsgi.application'


# Database
# https://docs.djangoprojec
# t.com/en/6.0/ref/settings/#databases

# POSTGRESQL DATABSE CONFIGRATION
DATABASES = {
    'default': {
        'ENGINE': config('DATABASE_ENGINE'),
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_PASSWORD'),
        'HOST': config('DATABASE_HOST'),
        'PORT': config('DATABASE_PORT')
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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
from django.utils.translation import gettext_lazy as _
import os
# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_L10N = True
USE_I18N = True
USE_TZ = True

LANGUAGE = [
    ('en', _('English')),
    ('so', _('Somali')),
    ('ar', _('Arabic')),
]
locale_path = os.path.join(BASE_DIR, 'locale')


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/
import os
STATIC_URL='static/'
STATICFILES_DIRS=[ 
    os.path.join(BASE_DIR, 'ecom/static')
]
STATIC_ROOT= os.path.join(BASE_DIR, 'staticfiles')

# MEDIA FILES CONFIGRATION
MEDIA_URL = 'media/'
MEDIA_ROOT= BASE_DIR / 'media'


# Messagess configration
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}


# SMTP configration Email
EMAIL_HOST =config('EMAIL_HOST')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD= config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool) 

# CART ID 
CART_SESSION_ID = 'cart'

# Redis configration
CACHES ={
    'default':{
        'BACKEND':'django_redis.cache.RedisCache',
        'LOCATION':'redis://127.0.0.1:6379/1',
        'OPTIONS':{
            'CLIENT_CLASS':'django_redis.client.DefaultClient'
            
        }
    }
}

# Celery URL
CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'