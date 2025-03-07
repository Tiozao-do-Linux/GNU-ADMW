## LDAP Autentication
#import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType, ldap

from core.settings import ENV

# LDAP Server Settings
AUTH_LDAP_SERVER_URI = ENV['AD_SERVER']
AUTH_LDAP_BIND_DN = ENV['AD_ADMIN_USER']
AUTH_LDAP_BIND_PASSWORD = ENV['AD_ADMIN_PASSWORD']

# Map LDAP attributes to Django user fields
AUTH_LDAP_USER_ATTR_MAP = {
    'username': 'sAMAccountName',
    'first_name': 'givenName',
    'last_name': 'sn',
    'email': 'mail',
}
# Where to find the users
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    'DC=grupoimagetech,DC=com,DC=br', # LDAP search base
    ldap.SCOPE_SUBTREE, # Scope
    '(sAMAccountName=%(user)s)', # LDAP search filter
)
# Options neededs
AUTH_LDAP_GLOBAL_OPTIONS = {
    ldap.OPT_PROTOCOL_VERSION: ldap.VERSION3,   # Use LDAPv3
    ldap.OPT_REFERRALS: 0, # Need for Active Directory
    ldap.OPT_X_TLS_REQUIRE_CERT : ldap.OPT_X_TLS_NEVER, # Never check for valid certificate
}
# Where to find the groups
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
    ENV['AD_SEARCH_BASE'], # LDAP search base
    ldap.SCOPE_SUBTREE,
    "(objectClass=groupOfNames)",
)
AUTH_LDAP_GROUP_TYPE = GroupOfNamesType(name_attr="cn")

# # Simple group restrictions
# AUTH_LDAP_REQUIRE_GROUP = "CN=Turma da Monica,CN=Users,DC=grupoimagetech,DC=com,DC=br"
# AUTH_LDAP_DENY_GROUP = "CN=Disabled,CN=Users,DC=grupoimagetech,DC=com,DC=br"

# # Define flags by group in LDAP
# AUTH_LDAP_USER_FLAGS_BY_GROUP = {
#     #"is_active": "CN=active,OU=django,OU=groups,DC=grupoimagetech,DC=com,DC=br",
#     "is_staff": "CN=Turma da Monica,CN=Users,DC=grupoimagetech,DC=com,DC=br",
#     #"is_superuser": "CN=superuser,OU=django,OU=groups,DC=grupoimagetech,DC=com,DC=br",
# }

# This is the default, but I like to be explicit.
AUTH_LDAP_ALWAYS_UPDATE_USER = True

# Use LDAP group membership to calculate group permissions.
AUTH_LDAP_FIND_GROUP_PERMS = True

# Cache distinguished names and group memberships for an hour to minimize LDAP traffic.
#AUTH_LDAP_CACHE_TIMEOUT = 3600

# Keep ModelBackend around for per-user permissions and maybe a local superuser.
#AUTHENTICATION_BACKENDS = (
#    'django_auth_ldap.backend.LDAPBackend',
#    'django.contrib.auth.backends.ModelBackend', # This is required for fallback
#)

# if 'AUTHENTICATION_BACKENDS' in globals():
#     AUTHENTICATION_BACKENDS = ( 'django_auth_ldap.backend.LDAPBackend', ) + AUTHENTICATION_BACKENDS
