
from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = True
ALLOWED_HOSTS = ['0,0,0,0','127.0.0.1','localhost']
INSTALLED_APPS = [ 'work.apps.workConfig']
ROOT_URLCONF = 'djangoProject.urls'
SECRET_KEY = "1234124"
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'xxgloq',
        'USER': 'xxgloq',
        'PASSWORD': 'root',
        'HOST': 'rm-wz9o1xqnj9614lmoy2o.mysql.rds.aliyuncs.com',
        'PORT': 3306,
    }
}
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/uploads/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
MEDIA_URL = '/uploads/'

MIDDLEWARE = [
    'work.middleware.auth.AuthMiddleware',
]

 