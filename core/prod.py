from .settings import *
import environ

env = environ.Env()

environ.Env.read_env()

DEBUG = False

SECRET_KEY = env.str("SECRET_KEY")

ALLOWED_HOSTS = tuple(env.list('ALLOWED_HOSTS'))

# Necesario para que request.scheme sea 'https' detrás de un proxy/nginx
# Sin esto, el canonical se genera como http:// en todos los templates
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache'),
        'KEY_PREFIX': 'wagtailcache',
        # 'TIMEOUT': 604800, # one week (in seconds)
    }
}