from django.forms import BaseModelForm
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from polls.models import Choice, Question, Vote
from django.views import generic
from django.views.generic import FormView ,CreateView
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import MemberForm, UserCreationForm 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.views import LogoutView, LoginView, PasswordResetView
from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import update_session_auth_hash

# Create your views here.
class RegisterView(generic.CreateView):
    form_class = MemberForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('polls:index')
    def form_valid(self, form):
        obj = form.save()
        obj.first_name = form.cleaned_data['first_name']
        obj.last_name = form.cleaned_data['last_name']
        obj.email = form.cleaned_data['email']
        return super().form_valid(form)

# # # ...
class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users:login')

class ChangePasswordView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/change_password.html'

# def change_password_view(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
                    
#             user = form.save()
#             messages.success(request,('Your password was successfully updated!'))
#             return redirect('users:change_password')
#         else:
#             messages.error(request,('Please correct the error below.'))
#     else:
#         form = PasswordChangeForm(request.user)
#     return render(request, 'users/change_password.html', {
#         'form': form
#     })


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = question.choice_set.all()
    # if not question.User(request.user):
    #     messages.error(
    #         request, "You already voted this poll!", extra_tags='alert alert-warning alert-dismissible fade show')
    #     return redirect("polls:list")
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        inputvalue = request.POST['choice']
        selected_choice = choices.get(id=inputvalue)
        selected_choice.votes = F("votes") + 1
        selected_choice.save()  
        Vote.objects.get_or_create(voter=request.user,
                                    choice=selected_choice)


# def login_view(request):
#     username = request.POST.get('username')
#     password = request.POST.get("password")
#     form = AuthenticationForm(initial={'username': None})
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 form = login(request, user)
#                 # Redirect to a success page.
#                 return redirect("polls:index")
#     return render(request, "users/login.html", 
#                   {"form":form})

class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('polls:index')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password= password)
        if user is not None:
            login(self.request,user)
            messages.success(self.request, f'Welcome {username}')
            # redirect to a success page
            return redirect('polls:index')
        return render(self.request, "users/login.html")



def logout_view(request):
    logout(request)
    messages.success(request, f'You were Logged Out')
    return redirect('users:login')



    
