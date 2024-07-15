from django.contrib import admin
from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views

app_name = "users"
urlpatterns = [
    path('register', views.RegisterView.as_view(), name ='register'),
    path('login', views.login_view, name ='login'),
    path('password_reset', views.ResetPasswordView.as_view(), name ='password_reset'),
    path('password_rest_subject', views.ResetPasswordView.as_view(), name ='password_reset_subject'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    path('logout', views.logout_view, name ='logout'),
    # path('logout', views.CustomLogoutView.as_view(), name='logout'),
]