from django.forms import BaseModelForm
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from .models import Choice, Question
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import MemberForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     context = {"latest_question_list": latest_question_list}
#     return render(request, "polls/index.html", context)

# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk = question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request, "polls/details.html", {"question": question})
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/detail.html", {"question": question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})  

# using generic views
class IndexView(LoginRequiredMixin, generic.ListView):
    login_url = "polls:login"
    redirect_field_name = "redirect_to"

    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5
    ]

class DetailView(LoginRequiredMixin,generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())
    
class ResultsView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = "polls/results.html"

class RegisterView(generic.CreateView):
    form_class = MemberForm
    template_name = 'polls/register.html'
    success_url = reverse_lazy('polls:index')

    def form_valid(self, form):
        obj = form.save()
        obj.first_name = form.changed_data_data['first_name']
        obj.last_name = form.changed_data_data['last_name']
        obj.email = form.changed_data_data['email']
        return super().form_valid(form)


# # # ...
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
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
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

# # views.py: Function to register user
def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get("password")
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                return redirect("polls:index")
            ...
    return render(request, "polls/login.html", 
                  {"form":form})

def logout_view(request):
    logout(request)
    return redirect('polls:login')

