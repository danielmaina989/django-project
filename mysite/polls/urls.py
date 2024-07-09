from django.contrib import admin
from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path('register', views.RegisterView.as_view(), name ='register'),
    path('login', views.login_view, name ='login'),
    path('password_rest', views.login_view, name ='password_reset'),
    # path('logout', views.logout_view, name ='logout'),
    path('logout', views.UserLogoutView.as_view(), name='logout'),
]
