from django.urls import path 
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('help/', HelpPageView.as_view(), name='help'),

#   path('login/', LoginView.as_view(), name='login'),
    path('logoff/', LogoffView.as_view(), name='logoff'),

    path('user/', UserListView.as_view(), name='user_list'),
    # path('user/<str:username>/create/', UserDetailView.as_view(), name='user_detail'),
    path('user/detail/<str:username>/', UserDetailUpdateView.as_view(), name='user_detail'),
    # path('user/update/<str:username>/', UserDetailUpdateView.as_view(), name='user_update'),
#    path('users/create/', views.user_create, name='user_create'),
#    path('users/<str:username>/reset-password/', views.user_reset_password, name='user_reset_password'),
#    path('user/<str:username>/disable/', views.user_disable, name='user_disable'), 
#    path('user/<str:username>/enable/', views.user_enable, name='user_enable'), 

     path('group/', GroupListView.as_view(), name='group_list'),
#    path('group/create/', views.group_create, name='group_create'), 
#    path('group/<str:group_name>/edit/', views.group_edit, name='group_edit'), 
#    path('group/<str:group_name>/delete/', views.group_delete, name='group_delete'), 
#    path('group/<str:group_name>/members/', views.group_members, name='group_members'), 
#    path('group/<str:group_name>/add_members/', views.group_add_members, name='group_add_members'), 
#    path('group/<str:group_name>/remove_members/', views.group_remove_members, name='group_remove_members'), 

     path('organization/', OrganizationListView.as_view(), name='organization_list'),

     path('computer/', ComputerListView.as_view(), name='computer_list'),

]

