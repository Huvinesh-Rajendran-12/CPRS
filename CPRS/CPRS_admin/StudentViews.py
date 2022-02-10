from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Project
from .decorators import student_required
from django.views.generic import CreateView
from .models import Student_Profile, Student, Task
from .forms import StudentProfileForm, TaskForm, UpdateTaskForm
import os
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
@login_required
@student_required
def student_dashboard(request):
    template_name = "student/student_dashboard.html"
    return render(request, template_name)

@login_required
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
        return redirect("student_view_profile")

@login_required
@student_required
def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            response = HttpResponse(f.read(), content_type="application/file")
            response["Content-Disposition"] = "attachment;filename=" + os.path.basename(
                file_path
            )
            return response
    raise Http404

@login_required
@student_required
def student_view_project_details(request):
    template_name = "student/view_project_details.html"
    project = Project.objects.get(group=request.user.student.group)
    client = Client.objects.get(id=project.client.id)
    context = {"project": project}
    return render(request, template_name, context)

def student_view_group_details(request):
    template_name = "student/view_group_details.html"
    group = StudentGroup.objects.get(id=request.user.student.group.id)
    students = Student.objects.filter(group=group)
    context = {"group":group,"students":students}
    return render(request,template_name,context)



@method_decorator(student_required, name='dispatch')
class TaskCreateView(CreateView, LoginRequiredMixin):
    model = Task
    form_class = TaskForm
    template_name = "student/task_form.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user.student 
        form.instance.project = self.request.user.student.group.project 

        return super().form_valid(form)

@student_required
def create_task(request):
    """logged in student can create task"""
    template_name = "student/task_form.html"
    if request.method == "GET":
        taskform = TaskForm(request.GET or None,request=request)
    elif request.method == "POST":
        taskform = TaskForm(request.POST,request=request)
        if taskform.is_valid():
            taskform.save()
        return redirect("student_view_task_list")
    context = {"form": taskform}
    return render(request, template_name, context)

@student_required
def update_task(request,task_id):
    """logged in student can create task"""
    template_name = "student/update_task_form.html"
    task = Task.objects.get(id=task_id)
    if request.method == "GET":
        updatetaskform = UpdateTaskForm(request.GET or None)
    elif request.method == "POST":
        updatetaskform = UpdateTaskForm(request.POST)
        if updatetaskform.is_valid():
            task.status = updatetaskform.cleaned_data.get("status")
            task.save()
        return redirect("student_view_task_list")
    context = {"form": updatetaskform}
    return render(request, template_name, context)

def student_view_task_list(request):
    tasks = Task.objects.filter(created_by=request.user.student) | Task.objects.filter(assigned_to=request.user.student)
    print(tasks)
    template_name = "student/student_view_task_list.html"
    context = {"tasks":tasks}
    return render(request,template_name,context)

