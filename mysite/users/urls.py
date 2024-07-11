from django.contrib import admin
from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views

app_name = "users"
urlpatterns = [
    path('register', views.RegisterView.as_view(), name ='register'),
    path('login', views.login_view, name ='login'),
    path('password_rest', views.login_view, name ='password_reset'),
    path('logout', views.logout_view, name ='logout'),
    # path('logout', views.CustomLogoutView.as_view(), name='logout'),
]