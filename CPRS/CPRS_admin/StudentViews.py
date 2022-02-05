from django.shortcuts import render
from django.http import HttpResponse
from .models import Project
from .decorators import student_required
import os


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


@student_required
def student_view_project_details(request):
    template_name = "student/view_project_details.html"
    project = Project.objects.get(group=request.user.student.group)
    context = {"project": project}
    return render(request, template_name, context)
