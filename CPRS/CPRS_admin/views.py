from django.shortcuts import render
from .forms import ProjectForm
from .forms import StudentForm
from django.views.generic import CreateView
from django.shortcuts import redirect
from django.contrib.auth import login
from .models import User

from .forms import StudentSignUpForm, ClientSignUpForm, SupervisorSignUpForm


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = "registration/signup.html"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = "student"

        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("")


class ClientSignUpView(CreateView):
    model = User
    form_class = ClientSignUpForm
    template_name = "registration/signup.html"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = "client"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()

        login(self.request, user)
        return redirect("")


class SupervisorSignUpView(CreateView):
    model = User
    form_class = SupervisorSignUpForm

    template_name = "registration/signup.html"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = "supervisor"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("")


def home_view(request):
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        # save the form data to model
        form.save()
    return render(request, "home.html", {"form": form})


def student_view(request):
    form = StudentForm(request.POST or None)
    if form.is_valid():
        # save the form data to model
        form.save()
    return render(request, "student.html", {"form": form})


def group_view(request):
    group = request.user.groups.all()
    print(group)
    print(request.user)
    return render(request, "group.html", {"group": group})

def admin_dashboard(request):
    return render(request, "main/dashboard.html")

def search(request):
    return render(request, "main/search.html")

def project(request):
    return render(request, "main/projects.html")

def student_dashboard(request):
    return render(request, "student/s_dashboard.html")

def supervisor_dashboard(request):
    return render(request, "supervisor/supervisor_dashboard.html")

def client_dashboard(request):
    return render(request, "client/client_dashboard.html")