from django.shortcuts import render
from .forms import ProjectForm
from .forms import StudentForm

def home_view(request):
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        # save the form data to model
        form.save()
    return render(request, "home.html", {'form':form})

def student_view(request):
    form = StudentForm(request.POST or None)
    if form.is_valid():
        # save the form data to model
        form.save()
    return render(request, "student.html", {'form':form})

def group_view(request):
    group = request.user.groups.all()
    print(group)
    print(request.user)
    return render(request,"group.html",{'group':group})
