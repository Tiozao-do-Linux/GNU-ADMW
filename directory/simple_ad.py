"""
This module facilitates interaction with AD using ms_active_directory
"""
import logging
logger = logging.getLogger(__name__)

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

from ms_active_directory import ADDomain

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
        self.session = None

        if not self.domain or not self.server or not self.user or not self.password:
            logger.critical(f'## Auth Error ##: Missing AD credentials')
            return None

        try:
            logger.debug(f'# Connect to Active Directory without discover by DNS') 
            self.ad_domain = ADDomain(self.domain, ldap_servers_or_uris=[self.server], discover_kerberos_servers=False, discover_ldap_servers=False)
            logger.debug(f'# Authenticate with account service with admin rights')
            self.session = self.ad_domain.create_session_as_user(user=self.user, password=self.password)
        except Exception as e:
            logger.critical(f'## Auth Error ##: {self.user} - {str(e)}')


    def __str__(self):
        return f"{self.domain} - {self.server} - {self.user}"
    

    def get_session(self):
        return self.session


    def get_domain(self):
        return self.ad_domain


    def get_user(self,
                 filter : str = None,
                 base : str = None,
                 attrs: List[str] = ['userPrincipalName', 'memberOf', 'cn', 'givenName', 'sn', 'mail']):
               
        user = None

        if base:
            self.session.set_domain_search_base(base)
        else:
            base = self.session.get_domain_search_base()

        logger.debug(f'# get_user({filter}, {base}, {attrs})')
        user = self.session.find_user_by_sam_name(filter, attrs)
        if not user:
            logger.critical(f'## User ({filter}) NOT found')
        else:
            logger.info(f'# User ({filter}) found ')

        return user


    def get_users(self,
                  filter : str = '*', 
                  base : str = None,
                  attrs: List[str] = None):
        
        users = None

        if base:
            self.session.set_domain_search_base(base)
        else:
            base = self.session.get_domain_search_base()

        logger.debug(f'# get_users({filter}, {base}, {attrs})')
        users = self.session.find_users_by_common_name(filter, attrs )
        #logger.info(f'# Found {len(users)} user(s)')
        return users


    def get_groups(self, 
                  filter : str = '*', 
                  base : str = None,
                  attrs: List[str] = ['member']):

        groups = None

        if base:
            self.session.set_domain_search_base(base)
                    
        logger.debug(f'# get_groups({filter}, {base}, {attrs})')
        groups = self.session.find_groups_by_common_name(filter, attrs )
        logger.info(f'# Found {len(groups)} group(s)')
        return groups


    def get_group_by_dn(self, 
                  filter : str = None,
                  attrs: List[str] = ['member']):

        group = None

        logger.debug(f'# get_group_by_dn({filter}, {attrs})')
        group = self.session.find_group_by_distinguished_name(filter, attrs)
        logger.info(f'# Group ({filter}) found')

        return group


    def login(self,
              filter: str = None,
              password: str = None):

        if not filter or not password:
            logger.critical(f'## Auth Error ##: Missing AD credentials')
            return None

        session = None

        # Try to authenticate creating a user session
        try:
            logger.debug(f'# Try Login into AD as {filter}')
            session = self.ad_domain.create_session_as_user(user=filter, password=password)
        except Exception as e:
            logger.critical(f'## Auth Error ##: {filter} - {str(e)}')

        logger.info(f'# Login ({filter}) successful')

        return session
