from django.forms import BaseModelForm
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import F, Count
from django.http import HttpResponse, HttpResponseRedirect
from polls.models import Choice, Question, Vote, Poll
from django.views import generic
from django.core.paginator import Paginator
from django.views.generic import FormView ,CreateView, ListView
from django.views.generic.edit import DeleteView
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserChangeForm
from users.forms import MemberForm, CreatePollForm, CreatePollQuizForm, CreatePollChoicesForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.views import LogoutView, LoginView, PasswordResetView
from django.conf import settings
from django.db.models import Q
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import update_session_auth_hash, get_user_model


# Create your views here.
class RegisterView(generic.CreateView):
    form_class = MemberForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('polls:index')

    
class ProfileEditView(UpdateView):
    form_class = UserChangeForm
    template_name = 'users/edit_profile.html'
    success_url = reverse_lazy('users:login')

    def get_object(self):
        return self.request.user
    

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

class EditPollView(UpdateView):
    model = Poll
    fields = ["name"]
    template_name = "users/edit_poll_name.html" 
    success_url = reverse_lazy('users:available_polls')



class PollDeleteView(DeleteView):
    model =Poll
    template_name = "users/delete_poll_name.html" 
    success_url = reverse_lazy("users:available_polls")



  
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
    
class EditQuizView(UpdateView):
    fields = ["question_text"]
    template_name = "users/edit_questions.html" 
    success_url = reverse_lazy('users:available_questions')
    queryset = Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")


class QuizDeleteView(DeleteView):
    model = Question
    template_name = "users/delete_question.html" 
    success_url = reverse_lazy("users:available_questions")


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

class AvailablePollsView(LoginRequiredMixin, ListView):
    form_class = CreatePollForm
    paginate_by= 4
    template_name = 'users/available_polls.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context["polls"] = Poll.objects.all()
        context["count"] = Poll.objects.count()
        return context
    def get_queryset(self):
        search_query = self.request.GET.get("search_poll")
        if search_query:
            object_list = Poll.objects.filter(
                name__icontains=search_query).order_by("-pub_date")
        else:
            object_list = Poll.objects.all()
        return object_list
    
class AvailableQuestionsView(LoginRequiredMixin, ListView):
    form_class = CreatePollForm
    paginate_by = 4
    model = Question
    template_name = 'users/available_questions.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context["questions"] = Question.objects.all()
        return context
    def get_queryset(self):  # new
        search_query = self.request.GET.get("search_quiz")
        if search_query:
            object_list = Question.objects.filter(
                question_text__icontains=search_query).order_by('-pub_date')
        else:
            object_list = Question.objects.all()
        return object_list
    
class VotersView(LoginRequiredMixin, ListView):
    login_url = "users:login"
    redirect_field_name = "redirect_to"
    model = Poll
    template_name = "users/voters.html"
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the Users
        # context["voters"] = Poll.objects.all()
        user = get_user_model()
        context["users"] = user.objects.all()
        context["votes"] = Vote.objects.annotate(Count('voter'))
        return context
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class PollsSearch(LoginRequiredMixin, ListView):
    model = Poll
    template_name = 'users/available_polls.html'
    context_object_name = 'polls'

    def get_queryset(self):  # new
        search_query = self.request.GET.get("search_poll")
        if search_query:
            object_list = Poll.objects.filter(
                Q(name__icontains=search_query) | Q(id__icontains=search_query)) 
        else:
            object_list = Poll.objects.all()
        return object_list

class QuizSearch(LoginRequiredMixin, ListView):
    model = Question
    template_name = 'users/available_questions.html'
    context_object_name = 'questions'

    def get_queryset(self):  # new
        search_query = self.request.GET.get("search_quiz")
        if search_query:
            object_list = Question.objects.filter(
                Q(question_text__icontains=search_query) | Q(id__icontains=search_query))
        else:
            object_list = Question.objects.all()
        return object_list
    
class VoterSearch(LoginRequiredMixin, ListView):
    model = Poll
    template_name = 'users/voters.html'
    context_object_name = 'users'
    def get_queryset(self):
        search_query = self.request.GET.get("search_voter") 
        user = get_user_model()   
        if search_query:
            object_list = user.objects.filter(
            Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query) | Q(email__icontains=search_query))
        else:
            object_list = user.objects.all()
        print(object_list)
        return object_list

    

