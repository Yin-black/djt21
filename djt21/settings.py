"""
Django settings for djt21 project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import sys



# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0,os.path.join(BASE_DIR,'apps'))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*u$#7(6a)_y$m0qp-%k&6$q-iw3%3!spug=t$^y1p+-k6sx5xq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#阿里云短信AK/SK
ACCESS_KEY_ID = "LTAIUNmZMjuV6f2k"
ACCESS_KEY_SECRET = "izKqv9rYlKSX6XjjhIro1DcEvPzVB1"

#阿里云签名或模板名
SIGN_NAME = "付帅帅"
TEMPLATES_CODE = "SMS_142947701"

#七牛云AK/SK
ACCESS_KEY = 'Uv-edxvVRIsfIc6Pqpx9oDcfof959q3uFxj2UR1P'
SECRET_KEY = 'bw3yxz8i0kbjGGEaWGk_fSB81Ac9J_1MS6taBT5H'

#七牛空间名称
BUCKET_NAME = 'pizizhu-image'

#每页显示的新闻数量
ONE_PAGE_NEWS_COUNT = 2

#百度云视频VOD
BAIDU_ACESS_KEY = 'fb393f97251e46b685d5f680a3689fcc'

BAIDU_SECRET_KEY = '15d1b6ad60be44f6b5e4b77a65642d51'

BAIDU_USER_KEY = '016bea81906c49aa'

BAIDU_USER_ID = 'a04f753283a143f9b45f8d28ede35c19'

#允计所有IP访问
ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'authPro.User'  #注册自定的User模型，代替系统自定义的User

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.news',
    'apps.course',
    'apps.doc',
    'apps.authPro',
    'apps.cms',
    'rest_framework',          #djangorestframework框架app
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

ROOT_URLCONF = 'djt21.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins' : ['django.templatetags.static'], #所有的模板可以直接使用static标签，不需要load static
        },
    },
]

WSGI_APPLICATION = 'djt21.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default':{
        'ENGINE' : 'django.db.backends.mysql',
        'NAME' : 'djt21',
        'USER' : 'admin',
        'PASSWORD' : 'Root110qwe',
        'HOST' : '127.0.0.1',
        'PORT' : 3306,
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR,'static'),]

#图片存储路径
MEDIA_URL = '/media/'
#项目根目录
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

#Banner图片存储路径
BANNER_URL = '/media/banner/'

#图片存储路径
DOC_URL = '/doc/'
#项目根目录
DOC_ROOT = os.path.join(BASE_DIR, 'doc')
