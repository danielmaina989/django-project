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
        views.PasswordResetView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/',views.PasswordResetView.as_view(),name='password_reset_complete'),
    path('logout', views.logout_view, name ='logout'),
     path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    # path('logout', views.CustomLogoutView.as_view(), name='logout'),
]