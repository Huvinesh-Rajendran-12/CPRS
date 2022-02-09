from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Project
from .decorators import student_required
from django.views.generic import CreateView
from .models import Student_Profile, Student
from .forms import StudentProfileForm
import os

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


