from pathlib import Path
from .config import ENV

# Basedir
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = ENV['SECRET_KEY']

DEBUG = ENV['DEBUG']

ALLOWED_HOSTS = ENV['ALLOWED_HOSTS']

CSRF_TRUSTED_ORIGINS = ENV['CSRF_TRUSTED_ORIGINS']

TIME_ZONE = ENV['TIME_ZONE']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 3rd Party
    'crispy_forms',
    'crispy_bootstrap5',
    # Local
    'accounts',
    'directory',
]

# Auth model user
AUTH_USER_MODEL = 'accounts.CustomUser'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'


# Database definition
if ENV['DATABASE_URL']:
    DATABASES = {
        'default': ENV['DATABASE_URL']
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = (
    ('en-us', 'English (US)'),
    ('pt-br', 'Português do Brasil'),
)

LOCALE_PATHS = [ BASE_DIR / 'locale', ]

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_DIR = [ BASE_DIR / 'static', ]
STATICFILES_DIRS = [ BASE_DIR / 'static', ]

# Media
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Crispy
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

#LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'about'
LOGOUT_REDIRECT_URL = 'home'

# Enable Password Reset via Email
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if DEBUG:
    # Enable logging for debug to console
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {"console": {"class": "logging.StreamHandler"}},
        "root": {"handlers": ["console"], "level": "DEBUG"},
    }
else:
    # Production settings
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Allow authentication through Active Directory
AUTHENTICATION_BACKENDS = [
    'core.auth_active_directory.ActiveDirectoryBackend',
    'django.contrib.auth.backends.ModelBackend', # This is required for fallback
]

