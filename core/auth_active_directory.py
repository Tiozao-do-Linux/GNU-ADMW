##from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib.auth.backends import BaseBackend

from ms_active_directory import ADDomain, logging_utils

logger = logging_utils.get_logger()

from .config import ENV

# Minimal configuration for Active Directory
AD_DOMAIN = ENV['AD_DOMAIN']
AD_SERVER = ENV['AD_SERVER']
AD_ADMIN_USER = ENV['AD_ADMIN_USER']
AD_ADMIN_PASSWORD = ENV['AD_ADMIN_PASSWORD']
AD_GROUP_REQUIRED = ENV['AD_GROUP_REQUIRED']
AD_GROUP_DENIED = ENV['AD_GROUP_DENIED']
#AD_USER_ATTRS = ENV['AD_USER_ATTRS']
#AD_GROUP_ATTRS = ENV['AD_GROUP_ATTRS']


class ActiveDirectoryBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            # Connect to Active Directory
            domain = ADDomain(AD_DOMAIN, ldap_servers_or_uris=[AD_SERVER], discover_kerberos_servers=False, discover_ldap_servers=False)
            # Authenticate with account service with admin rights
            session = domain.create_session_as_user(user=AD_ADMIN_USER, password=AD_ADMIN_PASSWORD)
        except Exception as e:
            logger.critical(f'## Auth Error ##: {AD_ADMIN_USER} - {str(e)}')
            return None

        # Find user by sAMAccountName
        user_ad = session.find_user_by_sam_name(username, ['givenName','sn','mail','userPrincipalName','memberOf'])
        if not user_ad:
            logger.critical(f'## User "{username}" NOT found')
            return None
        # else:
        #     logger.warning(f'Found User: {user_ad}')

        # Find required group by distinctiveName
        group_required = session.find_group_by_distinguished_name(AD_GROUP_REQUIRED, ['member'])
        if not group_required:
            logger.critical(f'## Required Group "{AD_GROUP_REQUIRED}" NOT found')
            dn_requiered_group = None
            return None
        else:
            dn_requiered_group = group_required.distinguished_name

        # Find denied group by distinctiveName
        group_denied = session.find_group_by_distinguished_name(AD_GROUP_DENIED, ['member'])
        if not group_denied:
            logger.warning(f'## Denied Group "{AD_GROUP_DENIED}" NOT found')
            dn_denied_group = None
        else:
            dn_denied_group = group_denied.distinguished_name

        # Map attributes from AD into Django user fields
            # 'first_name': 'givenName',
            # 'last_name': 'sn',
            # 'email': 'mail',
        userPrincipalName = user_ad.get('userPrincipalName')
        all_groups= user_ad.get('memberOf')
        givenName = user_ad.get('givenName')
        sn = user_ad.get('sn')
        mail = user_ad.get('mail')

        # Verify user is not a member of denied group and is a member of required group
        if all_groups:
            if dn_denied_group:
                if dn_denied_group in all_groups:
                    logger.warning(f'## User Denied: "{username}" is a member of "{AD_GROUP_DENIED}"')
                    return None
            elif dn_requiered_group in all_groups:
                # Try to authenticate creating a user session
                try:
                    user_session = domain.create_session_as_user(user=userPrincipalName, password=password)
                except Exception as e:
                    logger.error(f'## Auth Error ##: {username} - {str(e)}')
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

                #logger.info(f"Auth User: {user.username}")

                return user
            else:
                logger.warning(f'## User "{username}" NOT a member of "{AD_GROUP_REQUIRED}"')
                return None
        else:
            logger.warning(f'## User "{username}" NOT a member of any group')
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
