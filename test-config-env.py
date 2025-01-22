print(f'Read .env file\n======================================')

print(f'\n\tUsing dotenv:\n\t---------------------------------------')
# Import .env file - https://pypi.org/project/python-dotenv/
import os
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

AD_DOMAIN = os.getenv('AD_DOMAIN')
AD_SERVER = os.getenv('AD_SERVER')
AD_ADMIN_USER = os.getenv('AD_ADMIN_USER')
AD_ADMIN_PASSWORD = os.getenv('AD_ADMIN_PASSWORD')
AD_USER_ATTRS = os.getenv('AD_USER_ATTRS')
AD_GROUP_ATTRS = os.getenv('AD_GROUP_ATTRS')

print(f'\tAD_DOMAIN={AD_DOMAIN}\n\tAD_SERVER={AD_SERVER}\n\tAD_ADMIN_USER={AD_ADMIN_USER}\n\tAD_ADMIN_PASSWORD={AD_ADMIN_PASSWORD}\n\tAD_USER_ATTRS={AD_USER_ATTRS}\n\tAD_GROUP_ATTRS={AD_GROUP_ATTRS}')

print(f'\n\tUsing decouple:\n\t---------------------------------------')
# Import the config object: - https://pypi.org/project/python-decouple/

from decouple import config, Csv
# Retrieve the configuration parameters:
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

AD_DOMAIN = config('AD_DOMAIN',default='yourdomain.com')
AD_SERVER=config('AD_SERVER', default='ldaps://ip-or-dnsname')
AD_ADMIN_USER=config('AD_ADMIN_USER', default='admin@yourdomain.com')
AD_ADMIN_PASSWORD=config('AD_ADMIN_PASSWORD', default='password-of-admin')

AD_USER_ATTRS=config('AD_USER_ATTRS', default=[], cast=Csv())
AD_GROUP_ATTRS=config('AD_GROUP_ATTRS', default=[], cast=Csv())

print(f'\tAD_DOMAIN={AD_DOMAIN}\n\tAD_SERVER={AD_SERVER}\n\tAD_ADMIN_USER={AD_ADMIN_USER}\n\tAD_ADMIN_PASSWORD={AD_ADMIN_PASSWORD}\n\tAD_USER_ATTRS={AD_USER_ATTRS}\n\tAD_GROUP_ATTRS={AD_GROUP_ATTRS}')

