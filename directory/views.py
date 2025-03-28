#from django.conf import settings
from ms_active_directory import ADDomain, ADUser, ADGroup
from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone

from core.settings import ENV
#from .models import ADUser, ADGroup, AuditLog
from .forms import UserCreationForm, UserModificationForm

from directory.simple_ad import ConnectActiveDirectory, print_object

env_context = {
    'ad_domain' : ENV['AD_DOMAIN'],
    'ad_server' : ENV['AD_SERVER'],
    'ad_admin_user' : ENV['AD_ADMIN_USER'],
    'ad_user_attrs' : ENV['AD_USER_ATTRS'],
    'ad_group_attrs' : ENV['AD_GROUP_ATTRS'],
    'ad_base' : ENV['AD_BASE'],
    'ad_base_user' : ENV['AD_BASE_USER'],
    'ad_base_group' : ENV['AD_BASE_GROUP'],
    'ad_group_required' : ENV['AD_GROUP_REQUIRED'],
    'ad_group_denied' : ENV['AD_GROUP_DENIED'],
    'now' : timezone.now(),
}

## Template Views
#################

class HomePageView(TemplateView):
    template_name = 'home.html'

class AboutPageView(TemplateView):
    template_name = 'about.html'
    extra_context = env_context
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["now"] = timezone.now()
    #     return context

class HelpPageView(TemplateView):
    template_name = 'help.html'

# class LoginView(TemplateView):
#     template_name = 'login.html'
#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     return context

class LogoffView(TemplateView):
    template_name = 'logoff.html'


## List Views
##############

# User Management Views
class UserListView(ListView):
    template_name = 'users/list.html'
    # context_object_name = 'users'   # variable name used in template
    #extra_context = { "username" : filter }

    def get_queryset(self):
        
        filter = self.request.GET.get('filter')
        if not filter:
            filter = '*'
            return None

        con = ConnectActiveDirectory()
        users = con.get_users(filter=filter, attrs=['sAMAccountName','givenName','sn','mail','userAccountControl',
                                                    'lastLogonTimestamp','pwdLastSet','whenCreated','whenChanged', 'distinguishedName'])

        # Create list with some attributes
        user_list = [
            {
                'username':              user.get('sAMAccountName'),
                'givenName':             user.get('givenName'),
                'sn':                    user.get('sn'),
                'email':                 user.get('mail'),
                'status':                user.get('userAccountControl'),
                'lastLogonTimestamp':    user.get('lastLogonTimestamp'),
                'pwdLastSet':            user.get('pwdLastSet'),
                'whenCreated':           user.get('whenCreated'),
                'whenChanged':           user.get('whenChanged'),
                'distinguishedName':     user.distinguished_name, #user.get('distinguishedName'), #user.get_user_distinguished_name,
            }
            for user in users
        ]
        
        return user_list


class GroupListView(ListView):
    template_name = 'groups/list.html'
    #model = ADGroup
    # object_list -> ADGroup.objects.all()
    def get_queryset(self):
        pass

class ComputerListView(ListView):
    template_name = 'computers/list.html'
    #model = ADGroup
    # object_list -> ADGroup.objects.all()
    def get_queryset(self):
        pass

class OrganizationListView(ListView):
    template_name = 'organizations/list.html'
    #model = ADGroup
    # object_list -> ADGroup.objects.all()
    def get_queryset(self):
        pass

## Details Views
################

class UserDetailView(DetailView):
    template_name = 'users/detail.html'
    #model = ADUser
    # object -> ADUser.objects.get(pk=id)

    # def get_queryset(self):
    #     pass

    def get_object(self, queryset=None):
        filter = self.kwargs.get('username')

        con = ConnectActiveDirectory()
        users = con.get_user(filter=filter, attrs=ENV['AD_USER_ATTRS'])
        #print_object(users)

        if not users: return None

        return users.all_attributes
