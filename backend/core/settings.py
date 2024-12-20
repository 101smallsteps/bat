"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = "django-insecure-))-erl!t314d+a-*=k0!s7*mcjb+t$g3d+o=z%diw)7)9m(dr)"
SECRET_KEY = os.environ.get("SECRET_KEY")
# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True
DEBUG = bool(os.environ.get("DEBUG", default=0))
DOMAIN_NAME = 'bat4all.com'
#ALLOWED_HOSTS = ['localhost','http://localhost/','localhost:5173','http://localhost:5173/','http://127.0.0.1:5173/','127.0.0.1:5173']
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")

CORS_ORIGIN_ALLOW_ALL = True
#CORS_ORIGIN_ALLOW_ALL_ORIGINS = True
#CORS_ALLOWED_ORIGINS = [
# for react app
#    "http://localhost:5173",
#    'https://bat4all.com',
#    'https://core.bat4all.com',
#]

#CORS_ALLOW_METHODS = (
#    'GET',
#    'POST',
#    'PUT',
#    'PATCH',
#    'DELETE',
#    'OPTIONS',
#)

#CORS_EXPOSE_HEADERS = ['Content-Type', 'X-CSRFToken']
#CORS_ALLOW_CREDENTIALS = True

#CSRF_COOKIE_NAME = 'csrftoken'
#CSRF_COOKIE_DOMAIN = '.bat4all.com'

#SESSION_COOKIE_NAME = 'sessionid'
#SESSION_COOKIE_DOMAIN = '.bat4all.com'

#LANGUAGE_COOKIE_NAME = 'language'
#LANGUAGE_COOKIE_DOMAIN = '.bat4all.com'

SESSION_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE='None'
CSRF_COOKIE_SECURE = True
#CSRF_COOKIE_HTTPONLY = False
#SESSION_COOKIE_HTTPONLY = False


# CORS_ALLOWED_ORIGINS and CORS_ORIGIN_WHITELIST both serves same purpose , which ever works
CORS_ORIGIN_WHITELIST = [
    'https://bat4all.com',
    'http://localhost:5173'
]

#CSRF_TRUSTED_ORIGINS = ["http://localhost:1337"]
CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS").split(" ")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "rest_framework",
    "rest_framework.authtoken",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "corsheaders",
    "authentication.apps.AuthenticationConfig",
    "financials.apps.FinancialsConfig",
    "storages",
    "certification.apps.CertificationConfig",
    "teamtasks.apps.TeamtasksConfig"
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
	  'allauth.account.auth_backends.AuthenticationBackend',
    ]

WSGI_APPLICATION = "core.wsgi.application"

SITE_ID = 1

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
USE_SSL  = os.getenv('USE_SSL ') == 'TRUE'


if USE_SSL:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
USE_OCEAN_DB = os.getenv('USE_OCEAN_DB ') == 'TRUE'

if USE_OCEAN_DB :
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.getenv('POSTGRES_DB'),
            'USER': os.getenv('POSTGRES_USER'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
            'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
            'PORT': os.getenv('POSTGRES_PORT', '5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('POSTGRES_DB'),
            'USER': os.getenv('POSTGRES_USER'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
            'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
            'PORT': os.getenv('POSTGRES_PORT', '5432'),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Email settings

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "<your email host>"
EMAIL_USE_TLS = False
EMAIL_PORT = "<your email port>"
EMAIL_HOST_USER = "<your email user>"
EMAIL_HOST_PASSWORD = "<your email password>"
DEFAULT_FROM_EMAIL = "<your default from email>"


# djangorestframework
# https://www.django-rest-framework.org/

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication"
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}


# django-allauth
# https://django-allauth.readthedocs.io/

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_MAX_EMAIL_ADDRESSES = 2

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": "",
            "secret": "",
            "key": "",  # leave empty
        },
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
        "VERIFIED_EMAIL": True,
    }
}


def append_trailing_slash(url):
    return url if url[-1] == "/" else url + "/"


# <EMAIL_CONFIRM_REDIRECT_BASE_URL>/<key>
EMAIL_CONFIRM_REDIRECT_BASE_URL = append_trailing_slash(
    "http://localhost:3000/email/confirm/"
)
# <PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL>/<uidb64>/<token>/
PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL = append_trailing_slash(
    "http://localhost:3000/password-reset/confirm/"
)


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

USE_SPACES = os.getenv('USE_SPACES') == 'TRUE'

if USE_SPACES:

    AWS_ACCESS_KEY_ID = 'your_spaces_access_key'
    AWS_SECRET_ACCESS_KEY = 'your_spaces_secret_key'

    AWS_STORAGE_BUCKET_NAME = 'bat4all1'
    AWS_S3_ENDPOINT_URL = 'https://bat4all1.nyc3.digitaloceanspaces.com'
    AWS_S3_CUSTOM_DOMAIN = 'bat4all1.nyc3.digitaloceanspaces.com'
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    AWS_LOCATION = 'static'
    AWS_DEFAULT_ACL = 'public-read'

    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    STATIC_URL = '{}/{}/'.format(AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
    STATIC_ROOT = 'static/'
    STATICFILES_DIRS = [
        'core/static'
    ]
else:
################ DEV START
    STATIC_URL = '/static/'
    STATIC_ROOT = BASE_DIR /'staticfiles'
    STATICFILES_DIRS = [
        'core/static',
    ]
    STORAGES = {
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }



################ DEV END



MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

