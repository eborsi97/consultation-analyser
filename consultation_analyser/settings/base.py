"""
Django settings for consultation_analyser project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, ".env"), overwrite=False)

env = environ.Env(DEBUG=(bool, False))

SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env("DEBUG")

ALLOWED_HOSTS: list[str] = [os.getenv("DOMAIN_NAME", "0.0.0.0"), "*"]  # nosec

# Application definition

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.auth",
    "consultation_analyser.consultations",
    "compressor",
]


# TODO: steal code from this blog post to add a health check endpoint: https://testdriven.io/blog/deploying-django-to-ecs-with-terraform/#django-health-check

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "consultation_analyser.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        "APP_DIRS": True,
        "OPTIONS": {"environment": "consultation_analyser.jinja2.environment"},
    },
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
    },
]

WSGI_APPLICATION = "consultation_analyser.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

PRODUCTION_DEPLOYMENT = os.environ.get("PRODUCTION_DEPLOYMENT", False)

if PRODUCTION_DEPLOYMENT:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": os.getenv("DB_NAME"),
            "USER": os.getenv("DB_USER"),
            "PASSWORD": os.getenv("DB_PASSWORD"),
            "HOST": os.getenv("DB_HOST"),
            "PORT": 5432,
        }
    }
else:
    DATABASES = {"default": env.db()}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-gb"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

COMPRESS_PRECOMPILERS = (("text/x-scss", "django_libsass.SassCompiler"),)

STATIC_URL = "static/"
STATIC_ROOT = "frontend/"
STATICFILES_DIRS = [("govuk-assets", BASE_DIR / "node_modules/govuk-frontend/dist/govuk/assets")]
STATICFILES_FINDERS = [
    "compressor.finders.CompressorFinder",
    "django.contrib.staticfiles.finders.FileSystemFinder",
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


BATCH_JOB_QUEUE = env("BATCH_JOB_QUEUE")
BATCH_JOB_DEFINITION = env("BATCH_JOB_DEFINITION")
