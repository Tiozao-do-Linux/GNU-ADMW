"""
This module uses only ms-active-directory to interact to Active Directory
"""
import logging
logger = logging.getLogger(__name__)

# from ms_active_directory import ADDomain

from core.config import ENV

# Minimal configuration for Active Directory
AD_DOMAIN = ENV['AD_DOMAIN']
AD_SERVER = ENV['AD_SERVER']
AD_ADMIN_USER = ENV['AD_ADMIN_USER']
AD_ADMIN_PASSWORD = ENV['AD_ADMIN_PASSWORD']
AD_GROUP_REQUIRED = ENV['AD_GROUP_REQUIRED']
AD_GROUP_DENIED = ENV['AD_GROUP_DENIED']
AD_USER_ATTRS = ENV['AD_USER_ATTRS']
AD_GROUP_ATTRS = ENV['AD_GROUP_ATTRS']

from directory.simple_ad import ConnectActiveDirectory  #, print_object

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

class ActiveDirectoryBackend(BaseBackend):
    """
    The main backend class. This implements the auth backend API, although it
    actually delegates most of its work to ADUser
    """

    def get_user_model(self):
        """
        By default, this will return the model class configured by AUTH_USER_MODEL
        """
        return get_user_model()
    
    def authenticate(self, request, username=None, password=None):
        """
        Returns an authenticated Django user or None
        """

        # if username is None or password is None:
        #     logger.critical('## Auth Error ##: Missing username or password')
        #     return None

        con = ConnectActiveDirectory()
        if not con: return None
                
        user_ad = con.get_user(filter=username)
        if not user_ad: return None

        # Map attributes from AD into Django user fields
            # 'django_field': 'ad_field',
            #############################################
            # 'first_name': 'givenName',
            # 'last_name': 'sn',
            # 'email': 'mail',
        userPrincipalName = user_ad.get('userPrincipalName')
        all_groups= user_ad.get('memberOf')
        givenName = user_ad.get('givenName')
        sn = user_ad.get('sn')
        mail = user_ad.get('mail')

        # Find required group by distinctiveName
        group_required = con.get_group_by_dn(filter=AD_GROUP_REQUIRED)
        if not group_required:
            logger.critical(f'## Required Group "{AD_GROUP_REQUIRED}" NOT found')
            dn_requiered_group = None
            return None
        else:
            dn_requiered_group = group_required.distinguished_name

        # Find denied group by distinctiveName
        group_denied = con.get_group_by_dn(filter=AD_GROUP_DENIED)
        if not group_denied:
            logger.warning(f'## Denied Group "{AD_GROUP_DENIED}" NOT found')
            dn_denied_group = None
        else:
            dn_denied_group = group_denied.distinguished_name

        # Verify user is not a member of denied group and is a member of required group
        if all_groups:
            if dn_denied_group:
                if dn_denied_group in all_groups:
                    logger.warning(f'## User Denied: "{username}" is a member of "{AD_GROUP_DENIED}"')
                    return None
            elif dn_requiered_group in all_groups:
                user_session = con.login(userPrincipalName, password)
                if not user_session: return None

                # Create or retrieve user
                user, created = self.get_user_model().objects.get_or_create(username=username)

                if created:
                    # # user.is_staff = True
                    # # user.is_superuser = False
                    # # user.is_active = True
                    user.set_unusable_password()  # User is managed by AD, not by Django.

                # Always Update user attributes from AD
                if givenName: user.first_name = givenName
                if sn:        user.last_name = sn
                if mail:      user.email = mail
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
        user = None

        try:
            user = self.get_user_model().objects.get(pk=user_id)
        except user.DoesNotExist:
            pass

        return user

