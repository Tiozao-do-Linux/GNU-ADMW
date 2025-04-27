from directory.config import *
from directory.simple_ad import ConnectActiveDirectory, print_object

print(f'##############################################')
con = ConnectActiveDirectory()
if con.ad_session: print(con)

print(f'##############################################')
# user = con.get_user(filter='tiozao')
# # print(f'##>> get_user({user})')
# print_object(user)

new_values = {
    'givenName' : 'GivenName do Tiozao2',
    'sn' : 'Surname do Tiozao2',
    'employeeType' : 'Type do Tiozao2',
    'employeeNumber' : 'Number do Tiozao2',
}
success = con.update_user(filter='tiozao', update_attrs=new_values)

exit(0)



# print(f'##############################################')
# Filter_Users='Tiozao'
# users = con.get_users(filter=Filter_Users, attrs=['memberOf'])
# if not users:
#     print(f'## Users: "{Filter_Users}" NOT found')
# else:
#     for user in users:
#         print_object(user)


print(f'##############################################')
Filter_Group=GROUP_REQUIRED
group = con.get_group_by_dn(filter=Filter_Group)
if not group:
    print(f'## Required Group: "{Filter_Group}" NOT found')
else:
    print_object(group)

print(f'##############################################')
Filter_Group=GROUP_DENIED
group = con.get_group_by_dn(filter=Filter_Group)
if not group:
    print(f'## Denied Group: "{Filter_Group}" NOT found')
else:
    print_object(group)

print(f'##############################################')
Filter_User='tiozao'
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
    user_session = con.login(filter=Filter_User, password=ADMIN_PASSWORD)
    if user_session:
        print(f'## Login ({Filter_User}) Successfully ')
    else:
        print(f'## Login ({Filter_User}) Failed')

    print(f'##############################################')