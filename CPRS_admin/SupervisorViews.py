from .decorators import supervisor_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import (
    Supervisor_Profile,
    Supervisor,
    StudentGroup,
    Project,
    Student,
    Client,
    Task,
    StudentFeedback,
)
from .forms import SupervisorProfileForm, StudentFeedbackForm
from django.views.generic import CreateView
from .filters import TaskFilter

@login_required
@supervisor_required
def supervisor_dashboard(request):
    group_count = StudentGroup.objects.filter(
        supervisor=request.user.supervisor
    ).count()
    project_count = 0
    ongoing_project_count = 0
    completed_project_count = 0
    feedbacks = StudentFeedback.objects.filter(supervisor=request.user.supervisor)
    template_name = "supervisor/supervisor_dashboard.html"

    context = {
        "group_count": group_count,
        "project_count": project_count,
        "ongoing_project_count": ongoing_project_count,
        "completed_project_count": completed_project_count,
        "feedbacks":feedbacks
    }
    return render(request, template_name, context)


@login_required
@supervisor_required
def supervisor_view_profile(request):
    supervisor = Supervisor.objects.get(user=request.user)
    template_name = "supervisor/supervisor_view_profile.html"
    context = {"supervisor": supervisor}
    return render(request, template_name, context)


class SupervisorProfileEditView(CreateView):
    model = Supervisor_Profile
    form_class = SupervisorProfileForm
    template_name = "supervisor/edit_profile.html"

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.supervisor = Supervisor.objects.get(user=self.request.user)
        profile.save()
        return redirect("supervisor_view_profile")




@login_required
@supervisor_required
def supervisor_view_groups(request):
    groups = StudentGroup.objects.filter(supervisor=request.user.supervisor)
    template_name = "supervisor/supervisor_view_groups.html"
    context = {"groups": groups}
    return render(request, template_name, context)


@login_required
@supervisor_required
def supervisor_view_group_details(request, group_id):
    group = StudentGroup.objects.get(id=group_id)
    students = Student.objects.filter(group=group)
    project = Project.objects.get(id=group.project.id)
    client = Client.objects.get(id=group.client.id)
    template_name = "supervisor/supervisor_view_group_details.html"
    context = {
        "project": project,
        "students": students,
        "group": group,
        "client": client,
    }
    return render(request, template_name, context)


@login_required
@supervisor_required
def supervisor_view_group_progress(request, group_id):
    group = StudentGroup.objects.get(id=group_id)
    tasks = Task.objects.filter(group=group)
    task_filter = TaskFilter(request.GET, queryset=tasks)
    template_name = "supervisor/supervisor_view_group_progress.html"
    context = {"tasks": tasks, "task_filter": task_filter}
    return render(request, template_name, context)

@login_required
@supervisor_required
def supervisor_gives_feedback(request, task_id):
    """logged in supervisor can send feedback to student"""
    template_name = "supervisor/supervisor_gives_feedback.html"
    task = Task.objects.get(id=task_id)
    if request.method == "GET":
        feedbackform = StudentFeedbackForm(request.GET or None)
    elif request.method == "POST":
        feedbackform = StudentFeedbackForm(request.POST)
        if feedbackform.is_valid():
            feedback_message = feedbackform.cleaned_data.get("feedback")
            feedback = StudentFeedback.objects.create(supervisor=request.user.supervisor,task=task,feedback=feedback_message)
        return redirect("supervisor_view_groups")
    context = {"form": feedbackform}
    return render(request, template_name, context)

@login_required
@supervisor_required
def supervisor_archive_feedback(request,feedback_id):
    feedback = StudentFeedback.objects.get(id=feedback_id)
    feedback.is_archived = True
    feedback.save()
    return redirect("supervisor_dashboard")

@login_required
@supervisor_required
def supervisor_view_feedback_history(request):
    feedbacks = StudentFeedback.objects.filter(supervisor=request.user.supervisor)
    template_name = "supervisor/supervisor_view_feedback_history.html"
    context = {"feedbacks":feedbacks}
    return render(request,template_name,context)
