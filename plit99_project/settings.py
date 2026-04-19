import os
import secrets
from pathlib import Path
from urllib.parse import urlparse

import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_RUNTIME_DATA_DIR = BASE_DIR / '.runtime-data'


def env_bool(name, default=False):
    return os.getenv(name, str(default)).strip().lower() in {'1', 'true', 'yes', 'on'}


def env_int(name, default=0):
    raw_value = os.getenv(name, '').strip()
    if raw_value:
        return int(raw_value)
    return int(default)


def env_list(name, default=''):
    return [item.strip() for item in os.getenv(name, default).split(',') if item.strip()]


def env_path(name, default):
    raw_value = os.getenv(name, '').strip()
    if raw_value:
        path = Path(raw_value)
        return path if path.is_absolute() else (BASE_DIR / path).resolve()
    return default


SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_urlsafe(64))
DEBUG = env_bool('DEBUG', True)
ENABLE_DATABASE = env_bool('ENABLE_DATABASE', True)
BOOTSTRAP_DATABASE = env_bool('BOOTSTRAP_DATABASE', ENABLE_DATABASE)
DATA_DIR = env_path('APP_DATA_DIR', env_path('RENDER_DISK_PATH', DEFAULT_RUNTIME_DATA_DIR))
DATA_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_HOSTS = env_list('ALLOWED_HOSTS', '127.0.0.1,localhost')
render_hostname = os.getenv('RENDER_EXTERNAL_HOSTNAME')
if render_hostname and render_hostname not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(render_hostname)
render_external_url = os.getenv('RENDER_EXTERNAL_URL', '').strip()
if render_external_url:
    render_external_host = urlparse(render_external_url).hostname
    if render_external_host and render_external_host not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(render_external_host)

# Render can provision a new onrender.com hostname when the service is renamed
# or recreated. Accepting the platform subdomain keeps deploys from breaking on
# a stale hard-coded host value.
if os.getenv('RENDER') and '.onrender.com' not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append('.onrender.com')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core.apps.CoreConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'core.middleware.AdminDatabaseGuardMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'plit99_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'core' / 'templates'],
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

WSGI_APPLICATION = 'plit99_project.wsgi.application'

if ENABLE_DATABASE:
    DATABASES = {
        'default': dj_database_url.config(
            default=f"sqlite:///{(DATA_DIR / 'db.sqlite3').as_posix()}",
        )
    }
else:
    # Public pages can fall back to JSON snapshots when the database is disabled.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }

if DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
    DATABASES['default']['CONN_MAX_AGE'] = 0
    DATABASES['default']['OPTIONS'] = {
        'timeout': 30,
    }
else:
    DATABASES['default']['CONN_MAX_AGE'] = 600
    DATABASES['default']['CONN_HEALTH_CHECKS'] = True

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Asia/Bishkek'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = DATA_DIR / 'media'
MEDIA_ROOT.mkdir(parents=True, exist_ok=True)
SERVE_MEDIA_FILES = env_bool('SERVE_MEDIA_FILES', True)
LOCAL_MEDIA_MIRROR_ROOT = BASE_DIR / 'media'
LOCAL_MEDIA_MIRROR_ENABLED = env_bool('LOCAL_MEDIA_MIRROR_ENABLED', True)
if LOCAL_MEDIA_MIRROR_ENABLED:
    LOCAL_MEDIA_MIRROR_ROOT.mkdir(parents=True, exist_ok=True)

CONTENT_SNAPSHOT_DIR = env_path('CONTENT_SNAPSHOT_DIR', DATA_DIR / 'content_snapshot')
CONTENT_SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
PROJECT_CONTENT_SNAPSHOT_PATH = BASE_DIR / 'core' / 'fixtures' / 'site_content.json'

CSRF_TRUSTED_ORIGINS = env_list('CSRF_TRUSTED_ORIGINS')
if render_external_url and render_external_url not in CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS.append(render_external_url)
if render_hostname:
    render_origin = f'https://{render_hostname}'
    if render_origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(render_origin)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

default_session_engine = 'django.contrib.sessions.backends.signed_cookies' if os.getenv('RENDER') else 'django.contrib.sessions.backends.db'
SESSION_ENGINE = os.getenv('SESSION_ENGINE', default_session_engine)
default_message_storage = 'django.contrib.messages.storage.cookie.CookieStorage' if SESSION_ENGINE == 'django.contrib.sessions.backends.signed_cookies' else 'django.contrib.messages.storage.fallback.FallbackStorage'
MESSAGE_STORAGE = os.getenv('MESSAGE_STORAGE', default_message_storage)

SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_SSL_REDIRECT = env_bool('SECURE_SSL_REDIRECT', not DEBUG)
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = os.getenv('SECURE_REFERRER_POLICY', 'same-origin')
X_FRAME_OPTIONS = os.getenv('X_FRAME_OPTIONS', 'DENY')

SECURE_HSTS_SECONDS = env_int('SECURE_HSTS_SECONDS', 0)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool('SECURE_HSTS_INCLUDE_SUBDOMAINS', False)
SECURE_HSTS_PRELOAD = env_bool('SECURE_HSTS_PRELOAD', False)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
