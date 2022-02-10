import json
import requests
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import Client, Client_Request, StudentGroup, Project
from .forms import ClientRequestForm, ProjectForm , MLEClientProfileForm , IndustryClientProfileForm,UniversityClientProfileForm
from django.views.generic import CreateView
from .decorators import client_required



@client_required
def client_view_profile(request):
    user = request.user
    client = Client.objects.get(user=user)
    context = {"client":client}
    if client.client_type == "Industry":
        template_name = "client/industry_profile.html"
    elif client.client_type == "MLE":
        template_name = "client/mle_profile.html"
    elif client.client_type == "University":
        template_name = "client/university_profile.html"
    return render(
        request,
        template_name,
        context
    )


@client_required
def client_edit_profile(request):
    template_name = "client/client_edit_profile.html"
    user = request.user
    client = Client.objects.get(user=user)
    if client.client_type == "Industry":
        form = IndustryClientProfileForm
    elif client.client_type == "MLE":
        form = MLEClientProfileForm
    elif client.client_type == "University":
        form = UniversityClientProfileForm

    if request.method == "GET":
        profileform = form(request.GET or None)
    elif request.method == "POST":
        profileform = form(request.POST)
        if profileform.is_valid():
            profileform.client = request.user.client
            profileform.save()
        return redirect("client_view_profile")
    return render(
        request,
        template_name,
        {"form": form},
    )

# client requests to view group details
@client_required
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
@client_required
def client_view_requests(request):
    groups = StudentGroup.objects.get(client=request.user.client)
    context = {"groups": groups, "form": form}
    return render(request, "client/client_view_request.html", context)


# client views group details if given permission by the admin
@client_required
def client_view_group_details(request, group_id):
    group = StudentGroup.objects.get(id=group_id)
    context = {"group": group, "form": form}
    return render(request, "client/client_view_group_details.html", context)

@client_required
def client_view_groups(request):
    groups = StudentGroup.objects.get(client=request.user.client)
    context = {"groups": groups}
    return render(request, "client/client_view_group_list.html", context)


# clients views the list of projects
@client_required
def client_view_projects(request):
    template_name = "client/view_projects.html"
    projects = Project.objects.filter(client=request.user.client)
    context = {"projects": projects}
    return render(request, template_name, context)


# client adds the project
@client_required
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

            # for f in files:
            # file_instance = Project(id=project.id, file=f)
            # file_instance.save()
        return redirect("client_view_projects")
    context = {"form": form}
    return render(request, template_name, context)


@client_required
def client_dashboard(request):
    project_count = Project.objects.filter(client=request.user.client).count()
    completed_project_count = Project.objects.filter(client=request.user.client,status="Completed").count()
    ongoing_project_count = Project.objects.filter(client=request.user.client,status="Ongoing").count()
    not_assigned_project_count = Project.objects.filter(client=request.user.client,is_assigned=False).count()
    group_count = StudentGroup.objects.filter(client=request.user.client).count()
    template_name = "client/client_dashboard.html"

    context = {"project_count":project_count,"completed_project_count":completed_project_count,"ongoing_project_count":ongoing_project_count,"not_assigned_project_count":not_assigned_project_count,"group_count":group_count}
    return render(request, template_name,context)
