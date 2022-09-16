from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# No need for MEDIA_ROOT if using cloud
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
