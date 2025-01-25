# Install with 'pip install ms_active_directory'
from ms_active_directory import ADDomain

from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env
from decouple import config,Csv

print(f'# Retrieve the configuration parameters:')
AD_DOMAIN = config('AD_DOMAIN',default='yourdomain.com')
AD_SERVER=config('AD_SERVER', default='ldaps://ip-or-dnsname')
AD_ADMIN_USER=config('AD_ADMIN_USER', default='admin@yourdomain.com')
AD_ADMIN_PASSWORD=config('AD_ADMIN_PASSWORD', default='password-of-admin')

AD_USER_ATTRS=config('AD_USER_ATTRS', default=[], cast=Csv())
AD_GROUP_ATTRS=config('AD_GROUP_ATTRS', default=[], cast=Csv())

print(f'\tAD_DOMAIN={AD_DOMAIN}\n\tAD_SERVER={AD_SERVER}\n\tAD_ADMIN_USER={AD_ADMIN_USER}\n\tAD_ADMIN_PASSWORD={AD_ADMIN_PASSWORD}\n\tAD_USER_ATTRS={AD_USER_ATTRS}\n\tAD_GROUP_ATTRS={AD_GROUP_ATTRS}')

print(f'# Connect with AD_SERVER - {AD_SERVER} with {AD_ADMIN_USER} / {AD_ADMIN_PASSWORD}')
domain = ADDomain(AD_DOMAIN, ldap_servers_or_uris=[AD_SERVER])
session = domain.create_session_as_user(user=AD_ADMIN_USER, password=AD_ADMIN_PASSWORD)

# users and groups support a generic "get" for any attributes queried

print(f'# Find user by name="tiozao')
user = session.find_user_by_sam_name('tiozao', AD_USER_ATTRS)

print(f'# Display user info')
print()
print(f''.rjust(70,'='))
print(f'USER:'.ljust(10,'.'),f'{user.distinguished_name}')
print(f''.rjust(70,'='))
for attr in AD_USER_ATTRS:
    if user.get(attr) != None:
        print(attr.ljust(30,'-'),' : ',user.get(attr))

