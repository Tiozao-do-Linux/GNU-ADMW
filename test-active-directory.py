from core.config import ENV

from ms_active_directory import ADDomain

AD_ADMIN_PASSWORD = ENV['AD_ADMIN_PASSWORD']
AD_GROUP_REQUIRED = ENV['AD_GROUP_REQUIRED']
AD_GROUP_DENIED = ENV['AD_GROUP_DENIED']
AD_USER_ATTRS = ENV['AD_USER_ATTRS'] 
AD_GROUP_ATTRS = ENV['AD_GROUP_ATTRS']


print(f'##############################################')
from directory.simple_ad import ConnectActiveDirectory, print_object
con = ConnectActiveDirectory()
if con: print(con)

print(f'##############################################')
Filter_Users='*it*'
users = con.get_users(filter=Filter_Users, attrs=['memberOf'])
if not users:
    print(f'## Users: "{Filter_Users}" NOT found')
else:
    for user in users:
        print_object(user)

print(f'##############################################')
Filter_Groups='*monica*'
groups = con.get_groups(filter=Filter_Groups, attrs=['member'])
if not groups:
    print(f'## Groups: "{Filter_Groups}" NOT found')
else:
    for group in groups:
        print_object(group)

print(f'##############################################')
Filter_Group_DN=AD_GROUP_REQUIRED
group = con.get_group_by_dn(filter=Filter_Group_DN)
if not group:
    print(f'## Required Group: "{Filter_Group_DN}" NOT found')
else:
    print_object(group)

print(f'##############################################')
Filter_Group_DN=AD_GROUP_DENIED
group = con.get_group_by_dn(filter=Filter_Group_DN)
if not group:
    print(f'## Denied Group: "{Filter_Group_DN}" NOT found')
else:
    print_object(group)

print(f'##############################################')
Filter_User='monic*'
user = con.get_user(filter=Filter_User)
if not user:
    print(f'## User: "{Filter_User}" NOT found')
else:
    print_object(user)
    # get attributes
    userPrincipalName = user.get('userPrincipalName')
    givenName = user.get('givenName')
    sn = user.get('sn')
    memberOf = user.get('memberOf')
    mail = user.get('mail')

    print(f'##############################################')
    Filter_User=userPrincipalName
    user_session = con.login(filter=Filter_User, password=AD_ADMIN_PASSWORD)
    if user_session:
        print(f'## Login ({Filter_User}) Successfully ')
    else:
        print(f'## Login ({Filter_User}) Failed')

    print(f'##############################################')