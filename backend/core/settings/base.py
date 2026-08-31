# =============================================================
# IoT Environmental Monitoring — Django Base Settings
# Shared across all environments (local, production).
# Environment-specific overrides live in local.py / production.py
# =============================================================

from pathlib import Path
from decouple import config

# =============================================================
# PATHS
# =============================================================

# Absolute path to the backend/ directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# =============================================================
# SECURITY
# =============================================================

SECRET_KEY = config('DJANGO_SECRET_KEY')

DEBUG = config('DJANGO_DEBUG', cast=bool, default=False)

ALLOWED_HOSTS = config(
    'DJANGO_ALLOWED_HOSTS',
    default='localhost,127.0.0.1',
    cast=lambda v: [h.strip() for h in v.split(',')]
)


# =============================================================
# APPLICATIONS
# =============================================================

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    # REST API
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',

    # WebSocket support
    'channels',

    # Celery beat schedule stored in DB
    'django_celery_beat',

    # Django debug toolbar — active only in local.py
    # Listed here so migrations work across environments
    'debug_toolbar',
]

LOCAL_APPS = [
    'apps.devices',
    'apps.readings',
    'apps.alerts',
    'apps.commands',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# =============================================================
# MIDDLEWARE
# =============================================================

MIDDLEWARE = [
    # CORS headers must be first
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',

    # Serves static files efficiently without nginx in development
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# =============================================================
# URLS + WSGI/ASGI
# =============================================================

ROOT_URLCONF = 'core.urls'

WSGI_APPLICATION = 'core.wsgi.application'

# ASGI application — used by Daphne for HTTP + WebSocket
ASGI_APPLICATION = 'core.asgi.application'


# =============================================================
# TEMPLATES
# =============================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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


# =============================================================
# DATABASE — TimescaleDB (PostgreSQL)
# =============================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': config('POSTGRES_HOST', default='localhost'),
        'PORT': config('POSTGRES_PORT', cast=int, default=5432),
        'OPTIONS': {
            # Keeps DB connections alive between requests
            # Avoids connection overhead on every request
            'connect_timeout': 10,
        },
        'CONN_MAX_AGE': 60,
    }
}


# =============================================================
# DJANGO CHANNELS — WebSocket layer
# =============================================================

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [config('CHANNEL_LAYERS_REDIS_URL', default='redis://localhost:6379/1')],
        },
    },
}


# =============================================================
# CELERY — Task queue configuration
# =============================================================

CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Karachi'

# Use Django database to store the beat schedule
# Survives container restarts — schedule is not lost
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'


# =============================================================
# MQTT — Broker connection settings
# Read by the mqtt_subscriber management command and
# the command dispatcher service.
# =============================================================

MQTT_BROKER_HOST = config('MQTT_BROKER_HOST', default='localhost')
MQTT_BROKER_PORT = config('MQTT_BROKER_PORT', cast=int, default=1883)
MQTT_BACKEND_USERNAME = config('MQTT_BACKEND_USERNAME')
MQTT_BACKEND_PASSWORD = config('MQTT_BACKEND_PASSWORD')


# =============================================================
# DJANGO REST FRAMEWORK
# =============================================================

REST_FRAMEWORK = {
    # JWT authentication by default on all endpoints
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # All endpoints require login unless explicitly marked public
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    # Enable filtering, searching, ordering on all viewsets
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    # Pagination — prevents dumping thousands of readings at once
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
}


# =============================================================
# JWT SETTINGS
# =============================================================

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
    'AUTH_HEADER_TYPES': ('Bearer',),
}


# =============================================================
# CORS — Allow React dev server to call Django API
# =============================================================

CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:5173',
    cast=lambda v: [o.strip() for o in v.split(',')]
)

# Allow cookies and Authorization headers in cross-origin requests
CORS_ALLOW_CREDENTIALS = True


# =============================================================
# PASSWORD VALIDATION
# =============================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# =============================================================
# INTERNATIONALISATION
# =============================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Karachi'
USE_I18N = True
USE_TZ = True


# =============================================================
# STATIC FILES
# =============================================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# =============================================================
# DEFAULT PRIMARY KEY
# =============================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'