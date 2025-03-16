"""
This module facilitates interaction with AD with ms_active_directory
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

        try:
            # Connect to Active Directory without discover by DNS
            self.ad_domain = ADDomain(self.domain, ldap_servers_or_uris=[self.server], discover_kerberos_servers=False, discover_ldap_servers=False)
            # Authenticate with account service with admin rights
            self.session = self.ad_domain.create_session_as_user(user=self.user, password=self.password)
        except Exception as e:
            logger.critical(f'## Auth Error ##: {self.user} - {str(e)}')
            exit(1)

    def __str__(self):
        return f"{self.domain} - {self.server} - {self.user}"
    
    def get_session(self):
        return self.session

    def get_domain(self):
        return self.ad_domain

    def get_users(self,
                  filter : str = '*', 
                  base : str = None,
                  attrs: List[str] = None):
        
        users = None

        if base:
            self.session.set_domain_search_base(base)
        else:
            base = self.session.get_domain_search_base()

        if attrs:
            self.user_attrs = attrs

        logger.debug(f'get_users({filter}, {base}, {attrs})')
        print(f'# find_users_by_common_name="{filter}"')
        print(f'# base={base}')
        print(f'# attrs={attrs}')
        users = self.session.find_users_by_common_name(filter, attrs )
        print(f'# Found {len(users)} Users')
        return users
        
    def get_groups(self, 
                  filter : str = '*', 
                  base : str = None,
                  attrs: List[str] = None):

        groups = None

        if base:
            self.session.set_domain_search_base(base)
                    
        if attrs:
            self.group_attrs = attrs

        logger.debug(f'get_groups({filter}, {base}, {attrs})')
        print(f'# find_groups_by_common_name="{filter}"')
        print(f'# base={base}')
        print(f'# attrs={attrs}')
        groups = self.session.find_groups_by_common_name(filter, attrs )
        print(f'# Found {len(groups)} Groups')
        return groups
    
    def get_group_by_dn(self, 
                  filter : str = None,
                  attrs: List[str] = None):

        group = None

        if attrs:
            self.group_attrs = attrs

        logger.debug(f'get_group_by_dn_({filter}, {attrs})')
        print(f'# find_group_by_distinguished_name="{filter}"')
        print(f'# attrs={attrs}')
        group = self.session.find_group_by_distinguished_name(filter, attrs)
        print(f'# Found {group.distinguished_name}')
        return group
    

    def login(self, user: str, password: str):
        session = None

        # TODO: Check if user is in AD with groups restrictions
        try:
            print(f'# Try Login into AD as {user} / {password}')
            session = self.ad_domain.create_session_as_user(user=user, password=password)
        except Exception as e:
            logger.critical(f'## Auth Error ##: {user} - {str(e)}')
        return session
