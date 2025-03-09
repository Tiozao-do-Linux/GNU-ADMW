from core.config import ENV
from pprint import pprint
import json

# Install with 'pip install ms_active_directory'
from ms_active_directory import ADDomain

def print_AD_Object(object):
    if object:
        object = vars(object)
        distinguishedName = object['distinguished_name']
        print(f'='*80)
        print(f'OBJECT DN: {distinguishedName}')
        print(f'='*80)
        print(json.dumps(dict(object['all_attributes']), ensure_ascii=False, indent=3))
        print(f'-'*80)

# print(f'# Retrieve the configuration parameters:')
# print(f'-'*80)
# pprint(ENV)
# print(f'-'*80)

AD_DOMAIN = ENV['AD_DOMAIN']
AD_SERVER = ENV['AD_SERVER']
AD_ADMIN_USER = ENV['AD_ADMIN_USER']
AD_ADMIN_PASSWORD = ENV['AD_ADMIN_PASSWORD']
AD_USER_ATTRS = ENV['AD_USER_ATTRS'] 
AD_GROUP_ATTRS = ENV['AD_GROUP_ATTRS']
AD_GROUP_REQUIRED = ENV['AD_GROUP_REQUIRED']
AD_GROUP_DENIED = ENV['AD_GROUP_DENIED']

try:
    print(f'# Connect with {AD_DOMAIN} at {AD_SERVER} with user {AD_ADMIN_USER}')
    domain = ADDomain(AD_DOMAIN, ldap_servers_or_uris=[AD_SERVER], discover_kerberos_servers=False, discover_ldap_servers=False)
    session = domain.create_session_as_user(user=AD_ADMIN_USER, password=AD_ADMIN_PASSWORD)
except Exception as e:
    print(f'## Error: {str(e)}')
    exit(1)

print(f'# Find user by sAMAccountName="tiozao"')
user = session.find_user_by_sam_name('tiozao', AD_USER_ATTRS)
if not user:
    print(f'## User "tiozao" not found')
else:
    print_AD_Object(user)

print(f'# Find group by distinctiveName="{AD_GROUP_REQUIRED}"')
group = session.find_group_by_distinguished_name(AD_GROUP_REQUIRED, AD_GROUP_ATTRS)
if not group:
    print(f'## Group "{AD_GROUP_REQUIRED}" not found')
    exit(1)
else:
    print_AD_Object(group)
    dn_group = group.distinguished_name

# How to log into AD with a user belonging to a specific group
# 1): find the user
# 2): verifiy the user is a member of the group
# 3): log into AD as the user

# User to try login into AD
USER='monica'


print(f'# Find user by sAMAccountName="{USER}"')
user = session.find_user_by_sam_name(USER, ['memberOf'] )

if not user:
    print(f'## User "{USER}" not found')
else:
    print_AD_Object(user)

    all_groups = user.get("memberOf")
    dn_user = user.distinguished_name

    print(f'# Verify {USER} is a member of "{AD_GROUP_REQUIRED}"')
    if all_groups:
        if dn_group in all_groups:
            print(f'# {USER} is a member of "{AD_GROUP_REQUIRED}"')
            try:
                print(f'# Try Login into AD as {USER}')
                monica_session = domain.create_session_as_user(user=dn_user, password=AD_ADMIN_PASSWORD)
                print(f'# Login Successfully')
            except Exception as e:
                print(f'# Login Failed')
                print(f'## Error: {str(e)}')
        else:
            print(f'# {USER} is NOT a member of "{AD_GROUP_REQUIRED}"')
    else:
        print(f'# {USER} is NOT a member of any groups')

# Now find users and groups
USERS='c*'
print(f'# Find users by commonName="{USERS}"')
users = session.find_users_by_common_name(USERS, ['memberOf'] )
if not users:
    print(f'## Users "{USERS}" NOT found')
else:
    for user in users:
        print_AD_Object(user)

GROUPS='Turma*'
print(f'# Find groups by commonName="{GROUPS}"')
groups = session.find_groups_by_common_name(GROUPS, ['member'])
if not groups:
    print(f'## Groups "{GROUPS}" NOT found')
else:
    for group in groups:
        print_AD_Object(group)

# from core.auth_active_directory import ConnectActiveDirectory
# ad = ConnectActiveDirectory(AD_DOMAIN, AD_SERVER, AD_ADMIN_USER, AD_ADMIN_PASSWORD)
# Mask_Users='c*'
# users = ad.get_users(Mask_Users)
# if not users:
#     print(f'## Users "{Mask_Users}" NOT found')
# else:
#     for user in users:
#         print_AD_Object(user)
