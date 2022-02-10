from .decorators import supervisor_required
from django.shortcuts import render, redirect
from .models import Supervisor_Profile, Supervisor, StudentGroup, Project
from .forms import SupervisorProfileForm
from django.views.generic import CreateView
@supervisor_required
def supervisor_dashboard(request):
    group_count = StudentGroup.objects.filter(supervisor=request.user.supervisor).count()
    project_count = 0 
    ongoing_project_count = 0
    completed_project_count = 0 
    template_name = "supervisor/supervisor_dashboard.html"

    context = {"group_count":group_count,"project_count":project_count,"ongoing_project_count":ongoing_project_count,"completed_project_count":completed_project_count}
    return render(request, template_name,context)

@supervisor_required
def supervisor_view_profile(request):
    supervisor = Supervisor.objects.get(user=request.user)
    template_name = "supervisor/supervisor_view_profile.html"
    context = {"supervisor":supervisor}
    return render(request, template_name,context)

class SupervisorProfileEditView(CreateView):
    model = Supervisor_Profile
    form_class = SupervisorProfileForm
    template_name = "supervisor/edit_profile.html"

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.supervisor = Supervisor.objects.get(user=self.request.user)
        profile.save()
        return redirect("supervisor_view_profile")

@supervisor_required
def supervisor_view_groups(request):
    groups = StudentGroup.objects.filter(supervisor=request.user.supervisor)
    template_name = "supervisor/supervisor_view_groups.html"
    context = {"groups":groups}
    return render(request, template_name,context)

@supervisor_required
def supervisor_view_projects(request):
    groups = Project.objects.filter(group=request.user.supervisor.studentgroup)
    template_name = "supervisor/supervisor_view_groups.html"
    context = {"groups":groups}
    return render(request, template_name,context)
