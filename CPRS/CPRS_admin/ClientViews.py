import json
import requests
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import Client, Client_Request, StudentGroup, Project
from .forms import ClientRequestForm, ProjectForm
from django.views.generic import CreateView

# client requests to view group details
def client_request_group(request, group_id):
    template_name = "client/client_request_group.html"
    group = StudentGroup.objects.get(id=group_id)
    if request.method == "GET":
        requestform = ClientRequestForm(request.GET or None)
    elif request.method == "POST":
        requestform = StudentGroupModelForm(request.POST)
        if requestform.is_valid():
            requestform.client = request.user.client
            requestform.group = group
            requestform.save()
        return redirect("client_view_requests")
    context = {"group": group, "form": requestform}
    return render(request, "client/client_request_group.html", context)


# client views the details of the requests made so far
def client_view_requests(request):
    groups = StudentGroup.objects.get(client=request.user.client)
    context = {"groups": groups, "form": form}
    return render(request, "client/client_view_request.html", context)


# client views group details if given permission by the admin
def client_view_group_details(request, group_id):
    group = StudentGroup.objects.get(id=group_id)
    context = {"group": group, "form": form}
    return render(request, "client/client_view_group_details.html", context)


# clients views the list of projects
def client_view_projects(request):
    projects = Project.objects.get(client=request.user.client)
    context = {"projects": projects}
    return render(request, "client/view_projects", context)


# client adds the project
def add_project_view(request):
    template_name = "client/add_project.html"
    if request.method == "GET":
        form = ProjectForm(request.GET or None)
    elif request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        files = request.FILES.getlist("file")
        if form.is_valid():
            project = form.save(commit=False)
            project.client = request.user.client
            project.save()

            for f in files:
                file_instance = Project(id=project.id, file=f)
                file_instance.save()
        return redirect("client_view_projects")
    context = {"form": form}
    return render(request, template_name, context)
