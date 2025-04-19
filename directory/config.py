from dotenv import load_dotenv
from decouple import config, Csv
load_dotenv()

# Retrieve the configuration parameters from .env:
DOMAIN = config('DOMAIN',default='yourdomain.com')
SERVER = config('SERVER', default='ldaps://ip-or-dnsname')
ADMIN_USER = config('ADMIN_USER', default='admin@yourdomain.com')
ADMIN_PASSWORD = config('ADMIN_PASSWORD', default='password-of-admin')

USER_ATTRS = config('USER_ATTRS', default=[], cast=Csv())
GROUP_ATTRS = config('GROUP_ATTRS', default=[], cast=Csv())

SEARCH_BASE = config('SEARCH_BASE', default='DC=yourdomain,DC=com')
SEARCH_BASE_USER = config('SEARCH_BASE_USER', default='OU=Users,'+SEARCH_BASE)
SEARCH_BASE_GROUP = config('SEARCH_BASE_GROUP', default='OU=Groups,'+SEARCH_BASE)

GROUP_REQUIRED = config('GROUP_REQUIRED', default='CN=Turma da Monica,CN=Groups,'+SEARCH_BASE)
GROUP_DENIED = config('GROUP_DENIED', default='CN=Deny,OU=Groups,'+SEARCH_BASE)

import datetime
env_context = {
    'ad_domain' : DOMAIN,
    'ad_server' : SERVER,
    'ad_admin_user' : ADMIN_USER,
    'ad_user_attrs' : USER_ATTRS,
    'ad_group_attrs' : GROUP_ATTRS,
    'ad_search_base' : SEARCH_BASE,
    'ad_search_base_user' : SEARCH_BASE_USER,
    'ad_search_base_group' : SEARCH_BASE_GROUP,
    'ad_group_required' : GROUP_REQUIRED,
    'ad_group_denied' : GROUP_DENIED,
    'now' : datetime.datetime.now(),
}
