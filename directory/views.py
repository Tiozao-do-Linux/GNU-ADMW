# from django.conf import settings
from core.settings import ENV

from django.views.generic import TemplateView, ListView, DetailView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required, login_not_required


from django.contrib import messages
from django.utils import timezone
from directory.simple_ad import ConnectActiveDirectory, userAccountControl_is_enabled, extract_ou

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

class HelpPageView(LoginRequiredMixin, TemplateView):
    template_name = 'help.html'

class LoginView(TemplateView):
    template_name = 'login.html'

class LogoffView(TemplateView):
    template_name = 'logoff.html'


## List Views
##############

# User Management Views
class UserListView(ListView):
    template_name = 'users/list.html'


    def get_queryset(self):
        
        filter = self.request.GET.get('filter')

        if not filter: return None

        if '*' in filter:
            messages.warning(self.request, "Remove the character '*' from filter.")
            return None

        con = ConnectActiveDirectory()
        if not con.ad_session:
            messages.error(self.request, f"Unable to connect to Active Directory: {con}")
            return None

        users = con.get_users(filter=filter, attrs=['sAMAccountName','givenName','sn','mail','userAccountControl',
                                                    'lastLogonTimestamp','pwdLastSet','whenCreated','whenChanged',
                                                    'company', 'department', 'l', 'st', 'o'])

        if not users: return None

        # Create list with some attributes
        user_list = [
            {
                'username':              user.get('sAMAccountName'),
                'givenName':             user.get('givenName') if user.get('givenName') else '-',
                'sn':                    user.get('sn') if user.get('sn') else '',
                'email':                 user.get('mail') if user.get('mail') else '-',
                'userAccountControl':    user.get('userAccountControl'),
                'status':                userAccountControl_is_enabled(user.get('userAccountControl')),
                'lastLogonTimestamp':    user.get('lastLogonTimestamp'),
                'pwdLastSet':            user.get('pwdLastSet'),
                'whenCreated':           user.get('whenCreated'),
                'whenChanged':           user.get('whenChanged'),
                'distinguishedName':     user.distinguished_name,
                'lastOU':                extract_ou(user.distinguished_name),
                'company':               user.get('company'),
                'department':            user.get('department'),
                'l':                     user.get('l'),
                'st':                    user.get('st'),
                'o':                     user.get('o'),
            }
            for user in users
        ]
        
        return user_list


class GroupListView(ListView):
    template_name = 'groups/list.html'

    def get_queryset(self):
        pass

class ComputerListView(ListView):
    template_name = 'computers/list.html'

    def get_queryset(self):
        pass

class OrganizationListView(ListView):
    template_name = 'organizations/list.html'

    def get_queryset(self):
        pass

## Details Views
################

class UserDetailView(DetailView):
    template_name = 'users/detail.html'

    def get_object(self, queryset=None):
        filter = self.kwargs.get('username')

        con = ConnectActiveDirectory()
        if not con.ad_session: return None  # TODO redirect to error page

        users = con.get_user(filter=filter, attrs=['*'])

        if not users: return None

        return users.all_attributes
