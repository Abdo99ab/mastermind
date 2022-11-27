from split_settings.tools import include
import os
from dotenv import load_dotenv
load_dotenv()

ENV = os.getenv('DJANGO_ENV') or os.environ.get('DJANGO_ENV') or 'development'

base_settings = [
    'components/common.py',
    'environments/{}.py'.format(ENV),
]
include(*base_settings)
