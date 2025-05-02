from directory.config import *
from django.shortcuts import render, redirect

from django.views.generic import View, TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.decorators import login_required, permission_required, login_not_required

from django.contrib import messages
from directory.simple_ad import ConnectActiveDirectory, userAccountControl_is_enabled, extract_ou, clean_post_data

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

class UserToggleView(ListView):
    template_name = 'users/list.html'
    def get_queryset(self):
        filter = self.request.GET.get('filter')
        username = self.kwargs.get('username')
        messages.warning(self.request, f"Inside UserToggleView. Username: {username}")
        # return redirect('user_list')

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

class UserDetailView(LoginRequiredMixin, DetailView):
    template_name = 'users/detail.html'

    def get_object(self, queryset=None):
        filter = self.kwargs.get('username')

        con = ConnectActiveDirectory()
        if not con.ad_session: return None  # TODO redirect to error page

        users = con.get_user(filter=filter, attrs=['*'])

        if not users: return None

        return users.all_attributes


## Details/Update Views
################

from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
class UserUpdateView(UpdateView):
    template_name = 'users/detail.html'
    success_url = reverse_lazy('user_detail')

    def get(self, request, *args, **kwargs):
        username = self.kwargs.get('username')

        con = ConnectActiveDirectory()
        if not con.ad_session:
            return redirect('error_page')

        users = con.get_user(filter=username, attrs=['*'])
        if not users:
            return HttpResponseBadRequest('User not found.')

        # Create context
        context = {'object': users.all_attributes}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        username = self.kwargs.get('username')

        # Get data from form
        new_values = clean_post_data(request.POST)

        con = ConnectActiveDirectory()
        if not con.ad_session:
            return redirect('error_page')
        
        updated, updated_attrs = con.update_user(filter=username, update_attrs=new_values)
        if not updated:
            messages.warning(self.request, f"Username: {username} NOT updated")
        else:
            messages.success(self.request, f"Username: {username} updated sucessfully.\nUpdated attrs: {updated_attrs}")

        # messages.warning(self.request, f"Updated attrs: {updated_attrs}")


        # updated = con.ad_session.disable_account(username)
        # if not updated:
        #     return HttpResponseBadRequest('Error on disable.')
        # if not updated:
        #     return HttpResponseBadRequest('Error on update.')

        return redirect('user_detail', username=username)

