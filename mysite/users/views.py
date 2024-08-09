from django.forms import BaseModelForm
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from polls.models import Choice, Question, Vote, Poll
from django.views import generic
from django.views.generic import FormView ,CreateView, ListView
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from users.forms import MemberForm, CreatePollForm, CreatePollQuizForm, CreatePollChoicesForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.views import LogoutView, LoginView, PasswordResetView
from django.conf import settings
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import update_session_auth_hash, get_user_model


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

# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     choices = question.choice_set.all()
#     # if not question.User(request.user):
#     #     messages.error(
#     #         request, "You already voted this poll!", extra_tags='alert alert-warning alert-dismissible fade show')
#     #     return redirect("polls:list")
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST["choice"])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(
#             request,
#             "polls/detail.html",
#             {
#                 "question": question,
#                 "error_message": "You didn't select a choice.",
#             },
#         )
#     else:
#         inputvalue = request.POST['choice']
#         selected_choice = choices.get(id=inputvalue)
#         selected_choice.votes = F("votes") + 1
#         selected_choice.save()  
#         Vote.objects.get_or_create(voter=request.user,
#                                   choice=selected_choice)

class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('users:create_poll_name')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password= password)
        if user is not None:
            login(self.request,user)
            messages.success(self.request, f'Welcome {username}')
            # redirect to a success page
            return redirect('users:create_poll_name')
        return render(self.request, "users/login.html")

def logout_view(request):
    logout(request)
    messages.success(request, f'You were Logged Out')
    return redirect('users:login')


class CreatePollView(LoginRequiredMixin,CreateView):
    form_class = CreatePollForm
    template_name = 'users/create_poll_name.html'
    
    def form_valid(self, form):
        obj = form.save()
        messages.success(self.request, f'Your Poll was added succcesfully')
        # success_url = reverse_lazy('users:create_poll_quiz', kwargs={'poll_id': obj.id})
        # return redirect (success_url)
        return super().form_valid(form)
    
    def get_success_url(self, **kwargs):
        success_url = reverse_lazy('users:create_poll_quiz',
                                    kwargs={'poll_id': self.object.id})
        return success_url
    
class CreateQuizView(LoginRequiredMixin,CreateView):
    form_class = CreatePollQuizForm
    template_name = 'users/create_poll_quiz.html'
    def form_valid(self, form):
        obj = form.save() 
        messages.success(self.request, f'Your Question was added succcesfully')
        #success_url = reverse_lazy('users:create_poll_choice', kwargs={'question_id': obj.id})
        # success_url = f'/create_poll_quiz/{obj.id}/'
        # return redirect (success_url)
        return super().form_valid(form)
    def get_success_url(self, **kwargs):
        success_url = reverse_lazy('users:create_poll_choice',
                                    kwargs={'question_id': self.object.id})
        return success_url
    
       
class CreateChoicesView(LoginRequiredMixin,CreateView):
    form_class = CreatePollChoicesForm
    template_name = 'users/create_poll_choice.html'
    success_url = reverse_lazy('polls:index')
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.question_id = self.kwargs.get('question_id')
        obj.save()
        messages.success(self.request, f'Your Choice was added succcesfully')
        return super().form_valid(form)

@login_required
def available_polls(request):
    form = CreatePollForm()
    context = {'form' : form}
    context["polls"] = Poll.objects.all()
    return render(request, 'users/available_polls.html', context)
    # return redirect('users:create_poll_quiz')

@login_required   
def available_questions(request):
    form = CreatePollForm()
    context = {'form' : form}
    context["questions"] = Question.objects.all()
    return render(request, 'users/available_questions.html', context)
    # return redirect('users:create_poll_quiz')

class VotersView(LoginRequiredMixin, ListView):
    login_url = "users:login"
    redirect_field_name = "redirect_to"
    model = Poll
    template_name = "users/voters.html"
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the Users
        context["voters"] = Poll.objects.all()
        User = get_user_model()
        context["users"] = User.objects.all()
        return context
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

# @login_required 
# def voters(request):
#     context = {}
#     return render(request, 'users/voters.html', context)