from dotenv import load_dotenv
import os
load_dotenv()

MY_ENV = 'prod'
DEBUG = False

SECRET_KEY = os.getenv('SECRET_KEY') or os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = ["localhost","127.0.0.1"]

if "logs" not in os.listdir("."):
    os.mkdir("logs")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}