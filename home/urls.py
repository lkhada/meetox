from django.urls import path, include
from . import views
# from allauth.account.urls

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('logout', views.LogOut, name='logout'),
    path('user-details', views.UserDetails.as_view(), name='user-details'),
    path('set-user-public', views.SetUserPublic.as_view(), name='set-user-public'),
    path('set-user-admin', views.SetUserAdmin.as_view(), name='set-user-admin')
]