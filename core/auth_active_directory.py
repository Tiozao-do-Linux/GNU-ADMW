#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib.auth.backends import BaseBackend

#from ms_active_directory.environment.ldap.ldap_format_utils import *
from ms_active_directory import ADDomain

from core.config import ENV

# Minimal configuration for Active Directory
AD_DOMAIN = ENV['AD_DOMAIN']
AD_SERVER = ENV['AD_SERVER']
AD_ADMIN_USER = ENV['AD_ADMIN_USER']
AD_ADMIN_PASSWORD = ENV['AD_ADMIN_PASSWORD']

#AD_BASE = construct_ldap_base_dn_from_domain(AD_DOMAIN)

class ActiveDirectoryBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            # Connect to Active Directory
            domain = ADDomain(AD_DOMAIN, ldap_servers_or_uris=[AD_SERVER], discover_kerberos_servers=False, discover_ldap_servers=False)
            # Authenticate with account service
            session = domain.create_session_as_user(user=AD_ADMIN_USER, password=AD_ADMIN_PASSWORD)
            #session = domain.create_session_as_user(user=username, password=password)
        except Exception as e:
            print(f'## Error: {AD_ADMIN_USER} - {str(e)}')
            return None

        # Find user by sAMAccountName
        try:
            user_ad = session.find_user_by_sam_name(username, ['sAMAccountName','givenName','sn','mail','userPrincipalName'])
        except Exception as e:
            print(f'## Error: {username} - {str(e)}')
            return None
        else:
            print(f'## user_ad: {user_ad}')

        # Get attributes from AD
            # #map ldap attributes to Django user fields
            # 'username': 'sAMAccountName',
            # 'first_name': 'givenName',
            # 'last_name': 'sn',
            # 'email': 'mail',
        givenName = user_ad.get('givenName')
        sn = user_ad.get('sn')
        mail = user_ad.get('mail')

        if not user_ad:
            return None

        # Try to authenticate creating a user session
        try:
            user_session = domain.create_session_as_user(user=user_ad.get('userPrincipalName'), password=password)
        except Exception as e:
            print(f'## Error: {username} - {str(e)}')
            return None

        if not user_session.is_authenticated():
            return None

        # Create or retrieve user
        user, created = User.objects.get_or_create(username=username)
        if created:
            # # user.is_staff = True
            # # user.is_superuser = False
            # # user.is_active = True
            user.set_unusable_password()  # User is managed by AD, not by Django.

        # Always Update user attributes from AD
        if givenName: user.first_name = givenName
        if sn: user.last_name = sn
        if mail: user.email = mail
        user.save()

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
