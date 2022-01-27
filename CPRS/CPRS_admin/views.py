from django.shortcuts import render
from .forms import ProjectForm
from .forms import StudentForm
from django.views.generic import CreateView
from django.shortcuts import redirect
from django.contrib.auth import login
from .models import User, Project
from .decorators import * 
from .forms import StudentSignUpForm, ClientSignUpForm, SupervisorSignUpForm , ProjectForm


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
        return redirect("/login")


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
        return redirect("/login")


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
        return redirect("/login")


@client_required
class AddProjectView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "client/add_project.html"

    def form_valid(self,form):
        project = form.save()
        return project 

def home_view(request):
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        # save the form data to model
        form.save()
    return render(request, "home.html", {"form": form})


@student_required
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

@student_required
def student_dashboard(request):
    return render(request, "student/s_dashboard.html")

@supervisor_required
def supervisor_dashboard(request):
    return render(request, "supervisor/supervisor_dashboard.html")

def client_dashboard(request):
    return render(request, "client/client_dashboard.html")

def main_view(request):
    return render(request,"main/main.html")
