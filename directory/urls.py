from django.urls import path 
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('help/', HelpPageView.as_view(), name='help'),

    path('users/', UserListView.as_view(), name='user_list'),

#    path('login/', LoginView.as_view(), name='login'),
#    path('logout/', LogoutView.as_view(), name='logout'),

#    path('user', UserListView.as_view(), name='user_list'),
#    path('user/<str:username>/', UserDetailView.as_view(), name='user_detail'),

#    path('users/', views.user_list, name='user_list'),
#    path('users/create/', views.user_create, name='user_create'),
#    path('users/<str:username>/modify/', views.user_modify, name='user_modify'),
#    path('users/<str:username>/reset-password/', views.user_reset_password, name='user_reset_password'),
#    path('audit-log/', views.audit_log, name='audit_log'),

#    path('group', GroupListView.as_view(), name='group_list'),

#    path('organization', OrganizationListView.as_view(), name='organization_list'),

#    path('computer', ComputerListView.as_view(), name='computer_list'),

 #   path('user/create/', views.user_create, name='user_create'), 
#    path('user/<str:username>/edit/', views.user_edit, name='user_edit'), 
#    path('user/<str:username>/delete/', views.user_delete, name='user_delete'), 
#    path('user/<str:username>/password_reset/', views.password_reset, name='password_reset'), 
#    path('group/', group_list, name='group_list'), 
#    path('group/create/', views.group_create, name='group_create'), 
#    path('group/<str:group_name>/edit/', views.group_edit, name='group_edit'), 
#    path('group/<str:group_name>/delete/', views.group_delete, name='group_delete'), 
#    path('group/<str:group_name>/members/', views.group_members, name='group_members'), 
#    path('group/<str:group_name>/add_members/', views.group_add_members, name='group_add_members'), 
#    path('group/<str:group_name>/remove_members/', views.group_remove_members, name='group_remove_members'), 
#    path('computer/', computer_list, name='computer_list'),
#    path('group/', views.group, name='group'), 
#    path('computer/', views.computer, name='computer'), 
]

