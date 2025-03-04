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

# import logging
# logger = logging.getLogger(__name__)

env_context = {
    'ad_domain' : ENV['AD_DOMAIN'],
    'ad_server' : ENV['AD_SERVER'],
    'ad_admin_user' : ENV['AD_ADMIN_USER'],
    'ad_user_attrs' : ENV['AD_USER_ATTRS'],
    'ad_group_attrs' : ENV['AD_GROUP_ATTRS'],
    'ad_group_required' : ENV['AD_GROUP_REQUIRED'],
    'ad_group_deny' : ENV['AD_GROUP_DENY'],
    'now' : timezone.now(),
}

## Template Views
#################

class HomePageView(TemplateView):
    template_name = 'home.html'
    extra_context = env_context
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context

class AboutPageView(TemplateView):
    template_name = 'about.html'
    extra_context = env_context
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["now"] = timezone.now()
    #     return context

class HelpPageView(TemplateView):
    template_name = 'help.html'
    # extra_context = env_context
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context

# class LoginView(TemplateView):
#     template_name = 'login.html'
#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     return context

# class LogoutView(TemplateView):
#     template_name = 'logout.html'
#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     return context


## List Views
##############

# User Management Views
class UserListView(ListView):
    template_name = 'users/list.html'
    #model = ADUser
    paginate_by = 100 # if pagination is desired
    # object_list -> ADUser.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class GroupListView(ListView):
    template_name = 'groups/list.html'
    #model = ADGroup
    # object_list -> ADGroup.objects.all()

class ComputerListView(ListView):
    template_name = 'computers/list.html'
    #model = ADGroup
    # object_list -> ADGroup.objects.all()

class OrganizationListView(ListView):
    template_name = 'organizations/list.html'
    #model = ADGroup
    # object_list -> ADGroup.objects.all()

## Details Views
################

class UserDetailView(DetailView):
    template_name = 'users/detail.html'
    #model = ADUser
    # object -> ADUser.objects.get(pk=id)


class ADConnection:
    """Context manager for AD operations"""
    def __init__(self):
        self.domain = None

    def __enter__(self):
        # Initialize AD connection using current user's credentials
        self.domain = ADDomain()
        return self.domain

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Cleanup AD connection
        if self.domain:
            self.domain = None

# @login_required
# def user_list(request):
#     """View to list all AD users"""
#     search_query = request.GET.get('search', '')
    
#     with ADConnection() as domain:
#         # Get users from AD
#         users = domain.find_users(search_query) if search_query else domain.get_all_users()
        
#         # Convert AD users to our model format
#         user_list = [ADUser(
#             username=user.username,
#             first_name=user.first_name,
#             last_name=user.last_name,
#             email=user.email,
#             department=user.department,
#             enabled=user.is_enabled
#         ) for user in users]

#     # Pagination
#     paginator = Paginator(user_list, 25)
#     page = request.GET.get('page')
#     users = paginator.get_page(page)

#     return render(request, 'ad_manager/user_list.html', {'users': users, 'search_query': search_query})

# @login_required
# def user_create(request):
#     """View to create new AD user"""
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             try:
#                 with ADConnection() as domain:
#                     # Create user in AD
#                     user = domain.create_user(
#                         username=form.cleaned_data['username'],
#                         password=form.cleaned_data['password'],
#                         first_name=form.cleaned_data['first_name'],
#                         last_name=form.cleaned_data['last_name'],
#                         email=form.cleaned_data['email'],
#                         department=form.cleaned_data['department']
#                     )

#                     # Log the action
#                     AuditLog.objects.create(
#                         action='CREATE',
#                         actor=request.user,
#                         target_type='user',
#                         target_name=form.cleaned_data['username'],
#                         details=f"User created: {form.cleaned_data['username']}"
#                     )

#                 messages.success(request, f"User {form.cleaned_data['username']} created successfully!")
#                 return redirect('user_list')
#             except Exception as e:
#                 messages.error(request, f"Error creating user: {str(e)}")
#     else:
#         form = UserCreationForm()

#     return render(request, 'ad_manager/user_form.html', {'form': form, 'action': 'Create'})

# @login_required
# def user_modify(request, username):
#     """View to modify existing AD user"""
#     with ADConnection() as domain:
#         ad_user = domain.find_user(username)
#         if not ad_user:
#             messages.error(request, f"User {username} not found!")
#             return redirect('user_list')

#         if request.method == 'POST':
#             form = UserModificationForm(request.POST)
#             if form.is_valid():
#                 try:
#                     # Update user in AD
#                     ad_user.update(
#                         first_name=form.cleaned_data['first_name'],
#                         last_name=form.cleaned_data['last_name'],
#                         email=form.cleaned_data['email'],
#                         department=form.cleaned_data['department']
#                     )

#                     # Log the action
#                     AuditLog.objects.create(
#                         action='MODIFY',
#                         actor=request.user,
#                         target_type='user',
#                         target_name=username,
#                         details=f"User modified: {username}"
#                     )

#                     messages.success(request, f"User {username} updated successfully!")
#                     return redirect('user_list')
#                 except Exception as e:
#                     messages.error(request, f"Error updating user: {str(e)}")
#         else:
#             # Pre-fill form with current user data
#             form = UserModificationForm(initial={
#                 'first_name': ad_user.first_name,
#                 'last_name': ad_user.last_name,
#                 'email': ad_user.email,
#                 'department': ad_user.department
#             })

#     return render(request, 'ad_manager/user_form.html', {
#         'form': form, 
#         'action': 'Modify',
#         'username': username
#     })

# @login_required
# def user_reset_password(request, username):
#     """View to reset user password"""
#     if request.method == 'POST':
#         new_password = request.POST.get('new_password')
#         try:
#             with ADConnection() as domain:
#                 user = domain.find_user(username)
#                 if user:
#                     user.set_password(new_password)
                    
#                     # Log the action
#                     AuditLog.objects.create(
#                         action='PASSWORD',
#                         actor=request.user,
#                         target_type='user',
#                         target_name=username,
#                         details="Password reset performed"
#                     )
                    
#                     messages.success(request, f"Password reset successful for user {username}")
#                 else:
#                     messages.error(request, f"User {username} not found!")
#         except Exception as e:
#             messages.error(request, f"Error resetting password: {str(e)}")
        
#         return redirect('user_list')

#     return render(request, 'ad_manager/reset_password.html', {'username': username})

# @login_required
# def audit_log(request):
#     """View to display audit logs"""
#     logs = AuditLog.objects.all()
#     paginator = Paginator(logs, 50)
#     page = request.GET.get('page')
#     logs = paginator.get_page(page)
    
#     return render(request, 'ad_manager/audit_log.html', {'logs': logs})