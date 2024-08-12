from django.contrib import admin
from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views

app_name = "users"
urlpatterns = [
    path('register', views.RegisterView.as_view(), name ='register'),
    path('login', views.LoginView.as_view(), name ='login'),
    path('password_reset', views.ResetPasswordView.as_view(), name ='password_reset'),
    path('password_rest_subject', views.ResetPasswordView.as_view(), name ='password_reset_subject'),
    path('password_reset_confirm/<uidb64>/<token>/',
        views.PasswordResetView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/',views.PasswordResetView.as_view(),name='password_reset_complete'),
    path('logout', views.logout_view, name ='logout'),
    path('change_password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('create_poll_name/', views.CreatePollView.as_view(), name ='create_poll_name'),
    path('create_poll_quiz/<int:poll_id>/', views.CreateQuizView.as_view(), name ='create_poll_quiz'),
    path('create_poll_choice/<int:question_id>/', views.CreateChoicesView.as_view(), name ='create_poll_choice'),
    path('available_polls/', views.AvailablePollsView.as_view(), name ='available_polls'),
    # path('searched/', views.SearchViews.as_view(), name ='searched'),
    path('available_questions/', views.AvailableQuestionsView.as_view(), name ='available_questions'),
    path('voters', views.VotersView.as_view(), name ='voters'),
    path('pollsearch/', views.PollsSearch.as_view(), name='pollsearch'),
    path('quizsearch/', views.QuizSearch.as_view(), name='quizsearch'),
    path('votersearch/', views.VoterSearch.as_view(), name='votersearch'),

]