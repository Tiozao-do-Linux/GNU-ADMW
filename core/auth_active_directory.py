"""
This module uses only ms-active-directory to interact to Active Directory
"""

from django.contrib.auth import get_user_model
#User = get_user_model()

from ms_active_directory import ADDomain, ADUser, ADGroup, logging_utils

logger = logging_utils.get_logger()

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

from django.contrib.auth.backends import BaseBackend

class ActiveDirectoryBackend(BaseBackend):
    """
    The main backend class. This implements the auth backend API, although it
    actually delegates most of its work to ADUser and ADGroup
    """

    def get_user_model(self):
        """
        By default, this will return the model class configured by
        AUTH_USER_MODEL. Subclasses may wish to override it and return a proxy
        model.
        """
        return get_user_model()
    
    def authenticate(self, request, username=None, password=None):
        """
        Returns an authenticated Django user or None
        """

        if username is None or password is None:
            logger.critical('## Auth Error ##: Missing username or password')
            return None

        try:
            # Connect to Active Directory without discover by DNS
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
                user, created = self.get_user_model().objects.get_or_create(username=username)

                #user, created = User.objects.get_or_create(username=username)
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
        except user.ObjectDoesNotExist:
            pass

        return user

class ConnectActiveDirectory:
    def __init__(self, domain: str, server: str, user: str, password:str):
        self.domain = domain
        self.server = server
        self.user = user
        self.password = password
        try:
            # Connect to Active Directory without discover by DNS
            self.domain = ADDomain(self.domain, ldap_servers_or_uris=self.server, discover_kerberos_servers=False, discover_ldap_servers=False)
            # Authenticate with account service with admin rights
            self.session = self.domain.create_session_as_user(user=self.user, password=self.password)
        except Exception as e:
            logger.critical(f'## Auth Error ##: {self.user} - {str(e)}')
            self.session = None

    def __str__(self):
        return f"{self.domain} - {self.server} - {self.user}"
    
    def get_session(self):
        return self.session

    def get_domain(self):
        return self.domain

    def get_users(self, mask_users: str):
        users = None
        print(f'# Find Users by commonName="{mask_users}"')
        users = self.session.find_users_by_common_name(mask_users, ['memberOf'] )
        print(f'# Found {len(users)} Users')
        return users
        
    def get_groups(self, mask_groups: str):
        groups = None
        print(f'# Find Groups by commonName="{mask_groups}"')
        groups = self.session.find_groups_by_common_name(mask_groups, ['member'] )
        print(f'# Found {len(groups)} Groups')
        return groups
    
