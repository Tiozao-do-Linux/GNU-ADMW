# Install with 'pip install ms_active_directory'
from ms_active_directory import ADDomain

from core.settings import ENV

def print_AD_Object(object):
    import json
    object = vars(object)
    distinguishedName = object['distinguished_name']
    all_attributes = object['all_attributes']
    all_attributes_pretty = json.dumps(dict(all_attributes), ensure_ascii=False, indent=4)
    print(f''.rjust(80,'='))
    print(f'OBJECT DN:'.ljust(10,'.'),f'{distinguishedName}')
    print(f''.rjust(80,'='))
    print(all_attributes_pretty)
    print(f''.rjust(80,'-'))

print(f'# Retrieve the configuration parameters:')
AD_DOMAIN = ENV['AD_DOMAIN']
AD_SERVER = ENV['AD_SERVER']
AD_ADMIN_USER = ENV['AD_ADMIN_USER']
AD_ADMIN_PASSWORD = ENV['AD_ADMIN_PASSWORD']
AD_USER_ATTRS = ENV['AD_USER_ATTRS'] 
AD_GROUP_ATTRS = ENV['AD_GROUP_ATTRS']
AD_GROUP_CAN_VIEW = ENV['AD_GROUP_CAN_VIEW']

print(f'# Connect with AD_DOMAIN - {AD_DOMAIN} at AD_SERVER - {AD_SERVER} with {AD_ADMIN_USER}')
domain = ADDomain(AD_DOMAIN, ldap_servers_or_uris=[AD_SERVER])
session = domain.create_session_as_user(user=AD_ADMIN_USER, password=AD_ADMIN_PASSWORD)

print(f'# Find user by sAMAccountName="tiozao"')
user = session.find_user_by_sam_name('tiozao', AD_USER_ATTRS)
print(f'# Display user info')
print_AD_Object(user)

print(f'# Find group by sAMAccountName="{AD_GROUP_CAN_VIEW}"')
group = session.find_group_by_sam_name(AD_GROUP_CAN_VIEW, AD_GROUP_ATTRS)
print(f'# Display group info')
print_AD_Object(group)

# How to log into AD with a user belonging to a specific group
# 1): find the user
# 2): verifiy the user is a member of the group
# 3): log into AD as the user

print(f'# Find user by sAMAccountName="monica"')
monica_user = session.find_user_by_sam_name('monica', ['memberOf'] )

all_groups = monica_user.get("memberOf")
dn_user = monica_user.distinguished_name
dn_group = group.distinguished_name

print(f'# Verify monica_user is a member of "{AD_GROUP_CAN_VIEW}"')
if all_groups:
    if dn_group in all_groups:
        print(f'## Monica User is a member of "{AD_GROUP_CAN_VIEW}"')
        try:
            print(f'# Try Login into AD as monica_user')
            monica_session = domain.create_session_as_user(user=dn_user, password=AD_ADMIN_PASSWORD)
            print(f'# Login Successfully')
        except Exception as e:
            print(f'# Login Failed')
            print(f'## Error: {str(e)}')
    else:
        print(f'## Monica User is NOT a member of "{AD_GROUP_CAN_VIEW}"')
else:
    print(f'## Monica User is NOT a member of any groups')


