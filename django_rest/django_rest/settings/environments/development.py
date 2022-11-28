from dotenv import load_dotenv
import os
from django_rest.settings.components.common import BASE_DIR
load_dotenv()


MY_ENV = 'dev'
DEBUG = True
SECRET_KEY = os.getenv('SECRET_KEY') or os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = ["localhost","127.0.0.1"]

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'
STATIC_ROOT = BASE_DIR / 'static'
STATIC_URL = '/static/'