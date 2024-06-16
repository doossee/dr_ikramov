from pathlib import Path

from django.utils import timezone
import sys

try:
    from conf import settings
except ImportError:
    settings = None

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getattr(
    settings,
    "SECRET_KEY",
    "django-insecure-0ln2$jzy7-8!-f)+n7%iw!6)q^!dl$v9^=91qe@pv*v@tvy$o#",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getattr(settings, "DEBUG", True)

ALLOWED_HOSTS = getattr(settings, "ALLOWED_HOSTS", ["*"])
INTERNAL_IPS = getattr(settings, "INTERNAL_IPS", ["127.0.0.1"])

# SECURITY CERTIFICATE
SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    getattr(settings, "PROTOCOL", "http"),
)
SECURE_SSL_REDIRECT = getattr(settings, "SECURE_SSL_REDIRECT", False)
SESSION_COOKIE_SECURE = getattr(settings, "SESSION_COOKIE_SECURE", False)
CSRF_COOKIE_SECURE = getattr(settings, "CSRF_COOKIE_SECURE", False)

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": getattr(settings, "DB_ENGINE", "django.db.backends.sqlite3"),
        "NAME": getattr(settings, "DB_NAME", BASE_DIR / "db.sqlite3"),
        "USER": getattr(settings, "DB_USER", "postgres"),
        "PASSWORD": getattr(settings, "DB_PASSWORD", "12345"),
        "HOST": getattr(settings, "DB_HOST", "127.0.0.1"),
        "PORT": getattr(settings, "DB_PORT", "5432"),
    }
}


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd party package
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
    "django_filters",
    "debug_toolbar",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    # Project apps
    "src",
    "src.management",
    "src.treatment",
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

if DEBUG:
    MIDDLEWARE += [
        # 'core.middleware.ErrorMiddleware',
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]

ROOT_URLCONF = "core.urls"
WSGI_APPLICATION = "core.wsgi.application"
AUTH_USER_MODEL = "management.User"


# TEMPLATE settings
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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


# REST settings
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": (
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
        "django_filters.rest_framework.DjangoFilterBackend",
    ),
    "DEFAULT_PAGINATION_CLASS": "src.pagination.CustomPagination",
    "PAGE_SIZE": 30,
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "core.authentication.DevAuthentication",
        "core.authentication.TokenAuthentication",
    ],
    "COERCE_DECIMAL_TO_STRING": False,
}

SPECTACULAR_SETTINGS = {
    "TITLE": "dr_ikramov",
    "DESCRIPTION": "Dental clinic web-site backend",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_DIST": "SIDECAR",  # shorthand to use the sidecar instead
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timezone.timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timezone.timedelta(days=1),
    "TOKEN_OBTAIN_SERIALIZER": "src.serializers.CustomTokenObtainPairSerializer",
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]


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

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

NO_AVATAR = "/avatars/no_avatar.png"

STATIC_URL = "static/"
MEDIA_URL = "media/"

STATIC_ROOT = BASE_DIR / "static"
MEDIA_ROOT = BASE_DIR / "media"

FILE_UPLOAD_TEMP_DIR = BASE_DIR

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# SMS code verify
VERIFY_CODE_MINUTES = getattr(settings, "VERIFY_CODE_MINUTES", 5)

# REDIS related settings
REDIS_HOST = getattr(settings, "REDIS_HOST", "127.0.0.1")
REDIS_PORT = getattr(settings, "REDIS_PORT", "6379")
CELERY_BROKER_URL = "redis://" + REDIS_HOST + ":" + REDIS_PORT + "/0"
# BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = "redis://" + REDIS_HOST + ":" + REDIS_PORT + "/0"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}
