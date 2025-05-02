"""
This module facilitates interaction with AD using ms_active_directory
"""
from directory.config import *

from ms_active_directory import ADDomain, ADUser, ADGroup, ADObject

from typing import List
import logging
logger = logging.getLogger(__name__)
import json

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
    ou_parts = [part[3:] for part in parts if part.startswith(('OU=','CN='))]
    return ' > '.join(ou_parts)


def print_object(object):
    """
    Print object attributes like ldif format
    """
    if object:
        object = vars(object)
        distinguishedName = object['distinguished_name']
        print(f'='*80)
        print(f'Object DN: {distinguishedName}')
        print(f'-'*80)
        print(json.dumps(dict(object['all_attributes']), ensure_ascii=False, indent=3))
        print(f'-'*80)

from django.http import QueryDict
def clean_post_data(post_data: QueryDict):
    """
    Removes unwanted fields like csrf_token and empty values from POST and returns a clean dict.
    """
    exclude_fields = ['csrfmiddlewaretoken']
    return {
        k: v for k, v in post_data.items()
        if k not in exclude_fields #and v.strip() != ''
    }

class ConnectActiveDirectory:
    def __init__(self):

        self.domain = DOMAIN
        self.server = SERVER
        self.user = ADMIN_USER
        self.password = ADMIN_PASSWORD
        self.user_attrs = USER_ATTRS
        self.group_attrs = GROUP_ATTRS
        self.group_required = GROUP_REQUIRED
        self.group_denied = GROUP_DENIED

        self.ad_domain = None
        self.ad_session = None

        if not self.domain or not self.server or not self.user or not self.password:
            logger.critical(f'# Auth Error ##: Missing AD credentials')
            return None

        try:
            logger.debug(f'# Connect to Domain: {self.domain} on Ldap Server: {self.server}')
            self.ad_domain = ADDomain(self.domain, ldap_servers_or_uris=[self.server], discover_kerberos_servers=False, discover_ldap_servers=False)
            logger.debug(f'# Authenticate with {self.user} with admin rights')
            self.ad_session = self.ad_domain.create_session_as_user(user=self.user, password=self.password)
        except Exception as e:
            logger.critical(f'# Auth Error ##: {self.user} - {str(e)}')

            return None


    def __str__(self):
        return f"{self.domain} : {self.server} : {self.user}"


    def get_session(self):
        return self.ad_session


    def get_domain(self):
        return self.ad_domain


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

    """
    Update user.
      filter is the samAccountName
      update_attrs is a dictionary of attributes to update.
      return true on success and the updated attributes
    """
    def update_user(self,
                        filter : str = None,
                        base : str = None,
                        update_attrs: dict = None):

        # get only name of attrs of update_attrs to be updated instead of all ('*')
        attrs = update_attrs.keys()

        user = self.get_user(filter=filter, base=base, attrs=attrs)
        if not user:
            return [False, {}]

        # Get current values
        current_attrs = user.all_attributes

        modifications = {}
        for attr, new_value in update_attrs.items():
            current_value = current_attrs.get(attr)

            # Normalize values (ldap3 sometimes returns lists)
            if isinstance(current_value, list):
                current_value = current_value[0] if current_value else ''

            # Ignore same values
            if (current_value or '') == (new_value or ''):
                continue

            if new_value == '':
                # Erase if new_value is empty
                modifications[attr] = [] #'[(MODIFY_DELETE, [])]'
            else:
                # Replace
                modifications[attr] =  new_value #'[(MODIFY_REPLACE, [{new_value}])]'

        if not modifications:
            return [False, {}] # Nothing to do

        # print(f'## update_user ## ({filter}, {modifications})')

        success = self.ad_session.overwrite_attributes_for_user(filter, modifications, raise_exception_on_failure=False)
        if success:
            logger.info(f'# User ({filter}) updated. {modifications}')
        else:
            logger.critical(f'# User ({filter}) NOT updated. {modifications}')
        
        return [success, modifications]

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

        search_filter=f'(& (objectClass=user) (!(objectClass=computer)) (| (sAMAccountName={filter}) (cn={filter}) (givenName={filter}*) (sn={filter}*) (mail={filter}) (company={filter}) (department={filter}) (employeeNumber={filter}) ) )'

        logger.info(f'# get_users( {filter}, {base}, {attrs})')

        users = self.ad_session._find_ad_objects_and_attrs(base, search_filter, 'SUBTREE', attrs, 0, ADUser)
    
        if not users:
            logger.critical(f'# Users ({filter}) NOT found')
        else:
            logger.info(f'# Found {len(users)} user(s)')

        return users


    def get_groups(self, 
                  filter : str = None, 
                  base : str = None,
                  attrs: List[str] = ['member']):

        if not self.ad_session: return None

        groups = None

        if base:
            self.ad_session.set_domain_search_base(base)

        search_filter=f'(& (objectClass=group) (| (cn={filter}) (description={filter}) ) )'

        logger.debug(f'# get_groups({search_filter}, {base}, {attrs})')

        groups = self.ad_session._find_ad_objects_and_attrs(base, search_filter, 'SUBTREE', attrs, 0, ADGroup)

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

    def get_organizations(self, 
                  filter : str = None, 
                  base : str = None,
                  attrs: List[str] = ['member']):

        if not self.ad_session: return None

        organizations = None

        if base:
            self.ad_session.set_domain_search_base(base)

        search_filter=f'(& (objectClass=organizationalUnit) (| (ou={filter}) (description={filter}) ) )'
        #TODO: refactor

        logger.debug(f'# get_organizations( {search_filter}, {base}, {attrs})')

        organizations = self.ad_session._find_ad_objects_and_attrs(base, search_filter, 'SUBTREE', attrs, 0, ADObject)

        logger.info(f'# Found {len(organizations)} group(s)')

        return organizations


    def get_computers(self, 
                  filter : str = None, 
                  base : str = None,
                  attrs: List[str] = ['member']):

        if not self.ad_session: return None

        computers = None

        if base:
            self.ad_session.set_domain_search_base(base)

        search_filter=f'(& (objectClass=computer) (| (cn={filter}$) (description={filter}) ) )'

        logger.debug(f'# get_computers( {search_filter}, {base}, {attrs})')

        computers = self.ad_session._find_ad_objects_and_attrs(base, search_filter, 'SUBTREE', attrs, 0, ADUser)

        logger.info(f'# Found {len(computers)} group(s)')

        return computers


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
