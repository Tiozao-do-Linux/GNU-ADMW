#from django.conf import settings
from django.utils import timezone
from ms_active_directory import ADDomain, ADUser, ADGroup
from django.views.generic import TemplateView, ListView, DetailView
from core.settings import ENV

# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.http import JsonResponse

# from .forms import UserForm, GroupForm, PasswordResetForm
from .models import ADOperation

# import logging
# logger = logging.getLogger(__name__)

env_context = {
    'ad_domain' : ENV['AD_DOMAIN'],
    'ad_server' : ENV['AD_SERVER'],
    'ad_admin_user' : ENV['AD_ADMIN_USER'],
    'ad_user_attrs' : ENV['AD_USER_ATTRS'],
    'ad_group_attrs' : ENV['AD_GROUP_ATTRS'],
}

## Template Views
#################

class LoginView(TemplateView):
    template_name = 'login.html'
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context

class LogoutView(TemplateView):
    template_name = 'logout.html'
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context

class HomeView(TemplateView):
    template_name = 'home.html'
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context

class AboutView(TemplateView):
    template_name = 'about.html'
    extra_context = env_context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context

## List Views
##############

# User Management Views
class UserListView(ListView):
    template_name = 'directory/users/list.html'
    model = ADOperation
    paginate_by = 100 # if pagination is desired
    # object_list -> ADUser.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class GroupListView(ListView):
    template_name = 'directory/groups/list.html'
    model = ADGroup
    # object_list -> ADGroup.objects.all()

class ComputerListView(ListView):
    template_name = 'directory/computers/list.html'
    model = ADGroup
    # object_list -> ADGroup.objects.all()

class OrganizationListView(ListView):
    template_name = 'directory/organizations/list.html'
    model = ADGroup
    # object_list -> ADGroup.objects.all()

## Details Views
################

class UserDetailView(DetailView):
    template_name = 'directory/users/detail.html'
    model = ADUser
    # object -> ADUser.objects.get(pk=id)


# # User Management Views
# @login_required
# def user_list(request):
#     try:
#         domain = ADDomain(settings.AD_DOMAIN,ldap_servers_or_uris=[settings.AD_SERVER])
#         users = domain.get_users()
#         return render(request, 'directory/users/list.html', {'users': users})
#     except Exception as e:
#         messages.error(request, f"Error fetching users: {str(e)}")
#         return render(request, 'directory/users/list.html', {'users': []})

# @login_required
# def user_detail(request, username):
#     try:
#         domain = ADDomain(domain_name=settings.AD_DOMAIN)
#         user = domain.get_user(username)
#         if request.method == 'POST':
#             form = UserForm(request.POST)
#             if form.is_valid():
#                 # Update user attributes
#                 user.update(
#                     given_name=form.cleaned_data['first_name'],
#                     surname=form.cleaned_data['last_name'],
#                     email=form.cleaned_data['email'],
#                     enabled=form.cleaned_data['enabled']
#                 )
#                 ADOperation.objects.create(
#                     user=request.user,
#                     operation='modify_user',
#                     target=username,
#                     details=f"Modified user attributes"
#                 )
#                 messages.success(request, f"User {username} updated successfully")
#                 return redirect('user_list')
#         else:
#             form = UserForm(initial={
#                 'first_name': user.given_name,
#                 'last_name': user.surname,
#                 'email': user.email,
#                 'enabled': user.enabled
#             })
#         return render(request, 'directory/users/detail.html', {
#             'ad_user': user,
#             'form': form
#         })
#     except Exception as e:
#         messages.error(request, f"Error: {str(e)}")
#         return redirect('user_list')

# @login_required
# def user_create(request):
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#         if form.is_valid():
#             try:
#                 domain = ADDomain(domain_name=settings.AD_DOMAIN)
#                 new_user = domain.create_user(
#                     username=form.cleaned_data['username'],
#                     password=form.cleaned_data['password'],
#                     given_name=form.cleaned_data['first_name'],
#                     surname=form.cleaned_data['last_name'],
#                     email=form.cleaned_data['email']
#                 )
#                 ADOperation.objects.create(
#                     user=request.user,
#                     operation='create_user',
#                     target=form.cleaned_data['username']
#                 )
#                 messages.success(request, f"User {form.cleaned_data['username']} created successfully")
#                 return redirect('user_list')
#             except Exception as e:
#                 messages.error(request, f"Error creating user: {str(e)}")
#     else:
#         form = UserForm()
#     return render(request, 'directory/users/create.html', {'form': form})

# @login_required
# def user_delete(request, username):
#     if request.method == 'POST':
#         try:
#             domain = ADDomain(domain_name=settings.AD_DOMAIN)
#             user = domain.get_user(username)
#             user.delete()
#             ADOperation.objects.create(
#                 user=request.user,
#                 operation='delete_user',
#                 target=username
#             )
#             messages.success(request, f"User {username} deleted successfully")
#         except Exception as e:
#             messages.error(request, f"Error deleting user: {str(e)}")
#     return redirect('user_list')

# # Group Management Views
# @login_required
# def group_list(request):
#     try:
#         domain = ADDomain(domain_name=settings.AD_DOMAIN)
#         groups = domain.get_groups()
#         return render(request, 'directory/groups/list.html', {'groups': groups})
#     except Exception as e:
#         messages.error(request, f"Error fetching groups: {str(e)}")
#         return render(request, 'directory/groups/list.html', {'groups': []})

# @login_required
# def group_detail(request, group_name):
#     try:
#         domain = ADDomain(domain_name=settings.AD_DOMAIN)
#         group = domain.get_group(group_name)
#         members = group.get_members()
        
#         if request.method == 'POST':
#             form = GroupForm(request.POST)
#             if form.is_valid():
#                 group.update(
#                     display_name=form.cleaned_data['display_name'],
#                     description=form.cleaned_data['description']
#                 )
#                 ADOperation.objects.create(
#                     user=request.user,
#                     operation='modify_group',
#                     target=group_name
#                 )
#                 messages.success(request, f"Group {group_name} updated successfully")
#                 return redirect('group_list')
#         else:
#             form = GroupForm(initial={
#                 'display_name': group.display_name,
#                 'description': group.description
#             })
        
#         return render(request, 'directory/groups/detail.html', {
#             'group': group,
#             'members': members,
#             'form': form
#         })
#     except Exception as e:
#         messages.error(request, f"Error: {str(e)}")
#         return redirect('group_list')

# # Computer Management Views
# @login_required
# def computer_list(request):
#     try:
#         domain = ADDomain(domain_name=settings.AD_DOMAIN)
#         computers = domain.get_computers()
#         return render(request, 'directory/computers/list.html', {'computers': computers})
#     except Exception as e:
#         messages.error(request, f"Error fetching computers: {str(e)}")
#         return render(request, 'directory/computers/list.html', {'computers': []})

# # Password Reset View
# @login_required
# def password_reset(request, username):
#     if request.method == 'POST':
#         form = PasswordResetForm(request.POST)
#         if form.is_valid():
#             try:
#                 domain = ADDomain(domain_name=settings.AD_DOMAIN)
#                 user = domain.get_user(username)
#                 user.change_password(form.cleaned_data['new_password'])
#                 ADOperation.objects.create(
#                     user=request.user,
#                     operation='reset_password',
#                     target=username
#                 )
#                 messages.success(request, f"Password reset successful for {username}")
#                 return redirect('user_detail', username=username)
#             except Exception as e:
#                 messages.error(request, f"Error resetting password: {str(e)}")
#     else:
#         form = PasswordResetForm()
    
#     return render(request, 'directory/users/password_reset.html', {
#         'form': form,
#         'username': username
#     })

# # Group Membership Management
# @login_required
# def manage_group_membership(request, group_name):
#     if request.method == 'POST':
#         try:
#             domain = ADDomain(domain_name=settings.AD_DOMAIN)
#             group = domain.get_group(group_name)
#             action = request.POST.get('action')
#             username = request.POST.get('username')
            
#             user = domain.get_user(username)
            
#             if action == 'add':
#                 group.add_members([user])
#                 operation = 'add_to_group'
#             else:
#                 group.remove_members([user])
#                 operation = 'remove_from_group'
                
#             ADOperation.objects.create(
#                 user=request.user,
#                 operation=operation,
#                 target=f"{username} in {group_name}"
#             )
            
#             return JsonResponse({'status': 'success'})
#         except Exception as e:
#             return JsonResponse({'status': 'error', 'message': str(e)})
    
#     return JsonResponse({'status': 'error', 'message': 'Invalid request method'})