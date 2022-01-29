from django.shortcuts import render
from .forms import ProjectForm
from .forms import StudentForm
from django.views.generic import CreateView
from django.shortcuts import redirect
from django.contrib.auth import login, logout , authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import User, Project, Student_Profile, Student
from .decorators import * 
from .forms import StudentSignUpForm, ClientSignUpForm, SupervisorSignUpForm , ProjectForm, StudentProfileForm
from django.contrib.auth.decorators import login_required


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
        return redirect('signin')


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
        return redirect('signin')


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
        return redirect('signin')



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
    if request.user.is_authenticated and request.user.is_student:
        return render(request,'student/s_dashboard.html')
    elif request.user.is_authenticated and request.user.is_client:
        return redirect('client_dashboard')
    elif request.user.is_authenticated and request.user.is_supervisor:
        return redirect('supervisor_dashboard')
    else:
        return redirect('signin')

@supervisor_required
def supervisor_dashboard(request):
    if request.user.is_authenticated and request.user.is_student:
            return render(request,'student/s_dashboard.html')
    elif request.user.is_authenticated and request.user.is_client:
            return redirect('client_dashboard')
    elif request.user.is_authenticated and request.user.is_supervisor:
            return redirect('supervisor_dashboard')
    else:
        return redirect('signin')


@client_required
def client_dashboard(request):
    if request.user.is_authenticated and request.user.is_student:
            return render(request,'student/s_dashboard.html')
    elif request.user.is_authenticated and request.user.is_client:
            return redirect('client_dashboard')
    elif request.user.is_authenticated and request.user.is_supervisor:
            return redirect('supervisor_dashboard')
    else:
        return redirect('signin')


def signin(request):
    if request.user.is_authenticated:
        if request.user.is_student:
            return redirect('student_dashboard')
        if request.user.is_cleint:
            return redirect('client_dashboard')
        if request.user.is_supervisor:
            return redirect('supervisor_dashboard')
     
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username =username, password = password)
        print(user)
        if user is not None:
            login(request,user)
            if user.is_authenticated and user.is_student:               
                return redirect('student_dashboard') #Go to student home
            elif user.is_authenticated and user.is_client:                                                                                    
                return redirect('client_dashboard') #Go to teacher home      
            elif user.is_authenticated and user.is_supervisor:
                return redirect('supervisor_dashboard')

        else:
            form = AuthenticationForm()
            return render(request,'registration/login.html',{'form':form})
     
    else:
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form':form})


def main_view(request):
    return render(request,"main/main.html")

def student_profile_edit(request):
    form = StudentProfileForm(request.POST or None)
    if form.is_valid():
        # save the form data to model 
        form.save()
    return render(request, "student/student_profile.html", {"form": form})


class StudentProfileView(CreateView):
    model = Student_Profile
    form_class = StudentProfileForm
    template_name = "student/student_profile.html"

    def form_valid(self,form):
        profile = form.save(commit=False)
        profile.student = Student.objects.get(user=self.request.user)
        profile.save()
        return redirect('student_dashboard')

