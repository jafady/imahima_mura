"""
Django settings for imahima_mura project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
import datetime

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# # 環境変数からSECRET_KEYを取得する設定
SECRET_KEY = os.environ.get('SECRET_KEY')

# # 環境変数からDEBUGを取得。デフォルトはTrue（本番環境モード）
DEBUG = int(os.environ.get('DEBUG', default=0))

# # 許可するホストを記載
ALLOWED_HOSTS = ['localhost', '127.0.0.1','imahima-mura-server.herokuapp.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_yasg',
    
    'channels',

    # # Allauth用
    # 'django.contrib.sites', 
    # 'allauth',
    # 'allauth.account',
    # 'rest_auth',
    # 'rest_auth.registration',
    # 'allauth.socialaccount',

    'imahima',
]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

# JWT_AUTH = {
#     'JWT_VERIFY': True,
#     'JWT_VERIFY_EXPIRATION': True,
#     'JWT_LEEWAY': 0,
#     'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=86400),
#     'JWT_ALLOW_REFRESH': True,
#     'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
# }

CORS_ORIGIN_WHITELIST = (
    'http://localhost:8080',
    'http://localhost:8887',
    'https://imahima-mura.herokuapp.com',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'imahima_mura.urls'

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

WSGI_APPLICATION = 'imahima_mura.wsgi.application'
# websocket
ASGI_APPLICATION = "imahima_mura.asgi.application"
CHANNEL_LAYERS = {
    'default': {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        'CONFIG': {
            "hosts": [os.environ.get('REDIS_URL')]
        },
    },
}

# カスタムユーザ
AUTH_USER_MODEL = 'imahima.User'

# swagger
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
}

# # allAuth
# SITE_ID = 1
# AUTHENTICATION_BACKENDS = (
#     'allauth.account.auth_backends.AuthenticationBackend',  # 一般ユーザー用(メールアドレス認証)
#     'django.contrib.auth.backends.ModelBackend',  # 管理サイト用(ユーザー名認証)
# )
# ACCOUNT_AUTHENTICATION_METHOD = 'email'  # メールアドレス認証に変更する設定
# ACCOUNT_USERNAME_REQUIRED = False  # サインナップ、ログイン時のユーザーネーム認証をキャンセル
# ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # サインアップにメールアドレス確認を使用
# ACCOUNT_EMAIL_REQUIRED = True
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # ローカルでの開発のためメールをコンソールで表示する
# # LOGIN_REDIRECT_URL = 'imahima:home'  # ログイン成功後の遷移先の指定
# # ACCOUNT_LOGOUT_REDIRECT_URL = 'imahima:welcome'  # ログアウト成功後の遷移先の指定
# ACCOUNT_LOGOUT_ON_GET = True  # 確認を行わずログアウトする設定


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DATABASE_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('DATABASE_DB', os.path.join(BASE_DIR, 'db.sqlite3')),
        'USER': os.environ.get('DATABASE_USER', 'user'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'password'),
        'HOST': os.environ.get('DATABASE_HOST', 'localhost'),
        'PORT': os.environ.get('DATABASE_PORT', '5432'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'ja-jp'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
