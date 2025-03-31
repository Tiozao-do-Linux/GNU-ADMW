"""
This module facilitates interaction with AD using ms_active_directory
"""
import logging
logger = logging.getLogger(__name__)

def userAccountControl_is_enabled(uAC: int) -> bool:
    """
    Is Active if uAC in 512|544|66032|66048|66080|262656|262688|328192|328224
    The & operator compares each bit and set it to 1 if both are 1, otherwise it is set to 0:
    """
    return uAC & 2 == 0

def extract_ou(dn: str) -> str:
    """
      Returns where the user is in the structure
    """
    parts = dn.split(',')
    parts.pop(0)    # remove first element
    
    # grep for OUs or CN
    ou_parts = [part for part in parts if part.startswith(('OU=','CN='))]
    return ','.join(ou_parts)

import json
def print_object(object):
    if object:
        object = vars(object)
        distinguishedName = object['distinguished_name']
        print(f'='*80)
        print(f'Object DN: {distinguishedName}')
        print(f'-'*80)
        print(json.dumps(dict(object['all_attributes']), ensure_ascii=False, indent=3))
        print(f'-'*80)

from core.config import ENV

from ms_active_directory import ADDomain, ADUser, ADGroup

from typing import List

class ConnectActiveDirectory:
    def __init__(self):
        
        self.domain = ENV['AD_DOMAIN']
        self.server = ENV['AD_SERVER']
        self.user = ENV['AD_ADMIN_USER']
        self.password = ENV['AD_ADMIN_PASSWORD']
        self.user_attrs = ENV['AD_USER_ATTRS']
        self.group_attrs = ENV['AD_GROUP_ATTRS']
        self.group_required = ENV['AD_GROUP_REQUIRED']
        self.group_denied = ENV['AD_GROUP_DENIED']

        self.ad_domain = None
        self.ad_session = None
        self.ldap_session = None

        if not self.domain or not self.server or not self.user or not self.password:
            logger.critical(f'# Auth Error ##: Missing AD credentials')
            return None

        try:
            logger.debug(f'# Connect to Active Directory without discover by DNS') 
            self.ad_domain = ADDomain(self.domain, ldap_servers_or_uris=[self.server], discover_kerberos_servers=False, discover_ldap_servers=False)
            logger.debug(f'# Authenticate with account service with admin rights')
            self.ad_session = self.ad_domain.create_session_as_user(user=self.user, password=self.password)
            # session_user = self.ad_session.who_am_i()
            # print(f'# Authenticated as: {session_user}')

            self.ldap_session = self.ad_domain.create_ldap_connection_as_user(user=self.user, password=self.password)
            if self.ldap_session: print(f'## LDAP Session: {self.ldap_session} ##')


        except Exception as e:
            logger.critical(f'# Auth Error ##: {self.user} - {str(e)}')
            return None


    def __str__(self):
        return f"{self.domain} - {self.server} - {self.user}"
    

    def get_session(self):
        return self.ad_session


    def get_domain(self):
        return self.ad_domain


    def get_users(self,
                          filter : str = None,
                          base : str = None,
                          attrs: List[str] = None):

        if not self.ad_session: return None

        users = None

        if base:
            self.ad_session.set_domain_search_base(base)
        else:
            base = self.ad_session.get_domain_search_base()

        search_filter=f'(& (objectClass=user) (!(objectClass=computer)) (cn={filter}) )'

        print(f'# get_usersby_filter( {search_filter}, {base}, {attrs})')
        logger.info(f'# get_users_by_filter({filter}, {base}, {attrs})')

        users = self.ad_session._find_ad_objects_and_attrs(base, search_filter, 'SUBTREE', attrs, 0, ADUser)
        # print(f'## Found {len(users)} object(s)')
    
        if not users:
            logger.critical(f'# Users ({filter}) NOT found')
        else:
            logger.info(f'# Found {len(users)} user(s)')
            #logger.info(f'# Users ({filter}) found ')
        return users


    def get_user(self,
                 filter : str = None,
                 base : str = None,
                 attrs: List[str] = ['userPrincipalName', 'memberOf', 'cn', 'givenName', 'sn', 'mail']):

        if not self.ad_session: return None

        user = None

        if base:
            self.ad_session.set_domain_search_base(base)
        else:
            base = self.ad_session.get_domain_search_base()

        logger.debug(f'# get_user({filter}, {base}, {attrs})')
        user = self.ad_session.find_user_by_sam_name(filter, attrs)
        if not user:
            logger.critical(f'# User ({filter}) NOT found')
        else:
            logger.info(f'# User ({filter}) found ')

        return user


    def get_users_by_common_name(self,
                  filter : str = '*', 
                  base : str = None,
                  attrs: List[str] = None):

        if not self.ad_session: return None

        users = None

        if base:
            self.ad_session.set_domain_search_base(base)
        else:
            base = self.ad_session.get_domain_search_base()

        logger.debug(f'# get_users({filter}, {base}, {attrs})')
        #TODO - create a search_filter with cn, sn and mail
        # https://ms-active-directory.readthedocs.io/en/latest/ad_domain.html#creating-a-connection-with-the-addomain
        # https://ldap3.readthedocs.io/en/latest/searches.html
        
        # # This will search for all users with cn initialized with "M"
        # search_filter = '(& (objectClass=user) (!(objectClass=computer)) (cn=M*) )'

        # # This will search for all users that have an email address and sn initialized with "S*"
        # search_filter = '(& (objectClass=user) (!(objectClass=computer)) (sn=S*) (mail=*) )'

        # # This will search for all groups that initialize with "G"
        # search_filter = '(& (objectClass=group) (!(objectClass=person)) (cn=G*) )'

        # search_filter = '(& ({obj_class_attr}={obj_class}) ({attr}={attr_val}) )'
        
        # users_cn = self.session.find_users_by_attribute('l', 'Campo Grande', ['memberOf'])
        # users_cn = self.session.find_users_by_attribute('company', 'Grupo Imagetech', ['memberOf'])
        # users_cn = self.session.find_users_by_attribute('givenName', 'Jarbas', ['memberOf'])

        # users_cn = self.session.find_users_by_attribute('CPF', '50832875600', ['memberOf'])
        # print(f'Found {len(users_cn)} users_cn')

        # users_sn = self.session.find_users_by_attribute(attribute_name='sn', attribute_value=filter, attributes_to_lookup=attrs, size_limit=100 )
        # users_mail = self.session.find_users_by_attribute(attribute_name='mail', attribute_value=filter, attributes_to_lookup=attrs, size_limit=100 )
        # all_users = users_cn + users_sn + users_mail
        # all_users = users_cn
        # print_object(all_users)

        users = self.ad_session.find_users_by_common_name(filter, attrs )

        # Remove users with objectClass=computer
        for user in users:
            if 'computer' in user.get('objectClass'):
                # print_object(user)
                logger.info(f'# Remove Computer ({user.get("cn")})')
                users.remove(user)

        logger.info(f'# Found {len(users)} user(s)')
        return users


    def get_groups(self, 
                  filter : str = '*', 
                  base : str = None,
                  attrs: List[str] = ['member']):

        if not self.ad_session: return None

        groups = None

        if base:
            self.ad_session.set_domain_search_base(base)
                    
        logger.debug(f'# get_groups({filter}, {base}, {attrs})')
        groups = self.ad_session.find_groups_by_common_name(filter, attrs )
        logger.info(f'# Found {len(groups)} group(s)')
        return groups


    def get_group_by_dn(self, 
                  filter : str = None,
                  attrs: List[str] = ['member']):

        if not self.ad_session: return None

        group = None

        logger.debug(f'# get_group_by_dn({filter}, {attrs})')
        group = self.ad_session.find_group_by_distinguished_name(filter, attrs)
        if not group:
            logger.warning(f'# Group ({filter}) NOT found')
        else:
            logger.info(f'# Group ({filter}) found')

        return group


    def login(self,
              filter: str = None,
              password: str = None):

        if not self.ad_session: return None

        if not filter or not password:
            logger.critical(f'# Auth Error: Missing AD credentials')
            return None

        session = None

        # Try to authenticate creating a user session
        try:
            logger.debug(f'# Login as ({filter})')
            session = self.ad_domain.create_session_as_user(user=filter, password=password)
        except Exception as e:
            logger.critical(f'# Auth ({filter}) Error:  - {str(e)}')

        logger.info(f'# Login ({filter}) successful')

        return session
