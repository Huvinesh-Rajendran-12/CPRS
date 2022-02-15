from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Project
from .decorators import student_required
from django.views.generic import CreateView
from .models import Student_Profile, Student, Task, StudentGroup, Client, StudentFeedback
from .forms import StudentProfileForm, TaskForm, UpdateTaskForm, StudentFeedbackReplyForm
import os
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from .filters import TaskFilter

@login_required
@student_required
def student_dashboard(request):
    task_count = Task.objects.filter(group=request.user.student.group).count()
    tasks = Task.objects.filter(assigned_to=request.user.student)
    new_task_count = Task.objects.filter(
        group=request.user.student.group, status="New"
    ).count()
    completed_task_count = Task.objects.filter(
        group=request.user.student.group, status="Completed"
    ).count()
    ongoing_task_count = Task.objects.filter(
        group=request.user.student.group, status="Ongoing"
    ).count()
    template_name = "student/student_dashboard.html"

    context = {
        "task_count": task_count,
        "new_task_count": new_task_count,
        "completed_task_count": completed_task_count,
        "ongoing_task_count": ongoing_task_count,
        "tasks":tasks, 
    }
    return render(request, template_name, context)


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
def student_update_profile(request):
    profile = Student_Profile.objects.get(student=request.user.student)
    print(profile)
    form = StudentProfileForm(instance=profile)
    template_name = "student/student_profile.html"
    if request.method == "POST":
        form = StudentProfileForm(request.POST,instance=profile)
        if form.is_valid:
            form.save()
            return redirect("student_view_profile")
    context = {"form":form}
    return render(request,template_name,context)

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
    if request.user.student.has_group:
        if request.user.student.profile.group.has_project:
            template_name = "student/view_project_details.html"
            project = Project.objects.get(
                id=request.user.student.profile.group.project.id
            )
            client = Client.objects.get(id=project.client.id)
            context = {"project": project, "client": client}
            return render(request, template_name, context)
        else: 
            return HttpResponse("No projects assigned")
    else:
        return HttpResponse("No projects.")


def student_view_group_details(request):
    if request.user.student.has_group:
        template_name = "student/view_group_details.html"
        group = StudentGroup.objects.get(id=request.user.student.profile.group.id)
        students = Student.objects.filter(group=group)
        context = {"group": group, "students": students}
        return render(request, template_name, context)
    else:
        return HttpResponse("No group to view.")

@login_required
@student_required
def create_task(request):
    """logged in student can create task"""
    template_name = "student/task_form.html"
    if request.method == "GET":
        taskform = TaskForm(request.GET or None, request=request)
    elif request.method == "POST":
        taskform = TaskForm(request.POST, request=request)
        if taskform.is_valid():
            taskform.save()
        return redirect("student_view_task_list")
    context = {"form": taskform}
    return render(request, template_name, context)

@login_required
@student_required
def update_task(request, task_id):
    """logged in student can create task"""
    template_name = "student/update_task_form.html"
    task = Task.objects.get(id=task_id)
    if request.method == "GET":
        updatetaskform = UpdateTaskForm(request.GET or None,instance=task)
    elif request.method == "POST":
        updatetaskform = UpdateTaskForm(request.POST,instance=task)
        if updatetaskform.is_valid():
            task.status = updatetaskform.cleaned_data.get("status")
            task.save()
        return redirect("student_view_task_list")
    context = {"form": updatetaskform}
    return render(request, template_name, context)


@login_required
@student_required
def student_view_task_list(request):
    tasks = Task.objects.filter(created_by=request.user.student) | Task.objects.filter(
        assigned_to=request.user.student
    )
    task_filter = TaskFilter(request.GET,queryset=tasks)
    template_name = "student/student_view_task_list.html"
    context = {"tasks": tasks,"task_filter":task_filter}
    return render(request, template_name, context)

@login_required
@student_required
def student_reply_feedback(request,feedback_id):
    """logged in student can reply to feedback to supervisor"""
    template_name = "student/student_reply_feedback.html"
    feedback = StudentFeedback.objects.get(id=feedback_id)
    if request.method == "GET":
        feedbackreplyform = StudentFeedbackReplyForm(request.GET or None)
    elif request.method == "POST":
        feedbackreplyform = StudentFeedbackReplyForm(request.POST)
        if feedbackreplyform.is_valid():
            feedback_reply = feedbackreplyform.cleaned_data.get("feedback_reply")
            feedback.feedback_reply = feedback_reply
            feedback.save()
        return redirect("student_dashboard")
    context = {"form": feedbackreplyform}
    return render(request, template_name, context)

@login_required
@student_required
def student_view_feedback_history(request):
    template_name = "student/student_view_feedback_history.html"
    tasks = Task.objects.filter(assigned_to=request.user.student)
    context = {"tasks":tasks}
    return render(request,template_name,context)
