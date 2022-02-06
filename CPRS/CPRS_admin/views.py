from django.shortcuts import render
from .forms import ProjectForm
from .forms import StudentForm, StudentGroupModelForm
from django.views.generic import CreateView
from django.shortcuts import redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import User, Project, Student_Profile, Student
from .decorators import *
from .forms import (
    StudentSignUpForm,
    ClientSignUpForm,
    SupervisorSignUpForm,
    ProjectForm,
    StudentProfileForm,
    LoginForm,
)
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from django.contrib import messages
from django.urls import reverse
from dal import autocomplete 

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
        return redirect("login")


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
        return redirect("login")


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
        return redirect("login")


def admin_dashboard(request):
    return render(request, "main/dashboard.html")


def search(request):
    return render(request, "main/search.html")


def project(request):
    return render(request, "main/projects.html")


@student_required
def student_dashboard(request):
    template_name = "student/student_dashboard.html"
    return render(request, template_name)


@supervisor_required
def supervisor_dashboard(request):
    template_name = "supervisor/supervisor_dashboard.html"
    return render(request, template_name)


@client_required
def client_dashboard(request):
    template_name = "client/client_dashboard.html"
    return render(request, template_name)


def main_view(request):
    return render(request, "main/main.html")


@student_required
def StudentProfile(request):
    user = request.user
    student_profile = Student.objects.get(user=user)
    return render(
        request,
        "student/student_profile_view.html",
        {"student_profile": student_profile},
    )


class StudentProfileView(CreateView):
    model = Student_Profile
    form_class = StudentProfileForm
    template_name = "student/student_profile.html"

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.student = Student.objects.get(user=self.request.user)
        profile.save()
        return redirect("student_profile_view")


def LoginFormView(request):
    """log in the registered user"""
    template_name = "registration/login.html"
    if request.method == "GET":
        loginform = LoginForm(request.GET or None)
    elif request.method == "POST":
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            username = loginform.cleaned_data.get("username")
            password = loginform.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_student:
                    return redirect("student_dashboard")
                if user.is_client:
                    return redirect("client_dashboard")
                if user.is_supervisor:
                    return redirect("supervisor_dashboard")
                if user.is_superuser:
                    return redirect("admin_dashboard")
            else:
                messages.add_message(
                    request, messages.INFO, "Wrong credential,please try again"
                )

    context = {"form": loginform}
    return render(request, template_name, context)


def Logout(request):
    """logout logged in user"""
    logout(request)
    return redirect(reverse("main"))


def signup2(request):
    form = StudentSignUpForm
    return render(request, "registration/signup2.html", {"form": form})

class StudentNameAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Student.objects.none()

        qs = Student.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q,has_group=False)

        return qs
