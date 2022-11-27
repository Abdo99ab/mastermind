from dotenv import load_dotenv
import os
load_dotenv()

MY_ENV = 'dev'
DEBUG = True
SECRET_KEY = os.getenv('SECRET_KEY') or os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = ["localhost","127.0.0.1"]