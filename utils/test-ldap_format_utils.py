# https://github.com/zorn96/ms_active_directory/blob/main/ms_active_directory/environment/ldap/ldap_format_utils.py

from ms_active_directory.environment.ldap.ldap_format_utils import *

DOMAIN="sub1.sub2.sub3.tiozao.com"
BASE_DN="DC=tiozao,DC=com"
USER_NAME="John Doe"
USER_DN=f"CN={USER_NAME},OU=Users"
COMPUTER_NAME="computer01"
OBJECT_NAME="objeto"
OBJECT_LOCATION="users"

print(f'# construct_ldap_base_dn_from_domain({DOMAIN})', '==>',
      construct_ldap_base_dn_from_domain(DOMAIN))

print(f'# construct_domain_from_ldap_base_dn({BASE_DN})', '==>',
      construct_domain_from_ldap_base_dn(BASE_DN))

print(f'# is_dn({USER_DN})', '==>',
      is_dn(USER_DN))

print(f'# strip_domain_from_canonical_name({USER_DN},{DOMAIN})', '==>',
      strip_domain_from_canonical_name(USER_DN, DOMAIN))

print(f'# convert_to_ldap_iterable({USER_DN})', '==>',
      convert_to_ldap_iterable(USER_DN))

print(f'# construct_default_hostnames_for_computer({COMPUTER_NAME},{DOMAIN})', '==>',
      construct_default_hostnames_for_computer(COMPUTER_NAME, DOMAIN))

print(f'# construct_object_distinguished_name({OBJECT_NAME},{OBJECT_LOCATION},{DOMAIN})', '==>',
      construct_object_distinguished_name(OBJECT_NAME,OBJECT_LOCATION,DOMAIN))

