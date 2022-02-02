import json
import requests
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import Client,Client_Request, StudentGroup, Project 
from .forms import ClientRequestForm, ProjectForm
from django.views.generic import CreateView

def client_request_group(request,group_id):
    template_name = "client/client_request_group.html"
    group = StudentGroup.objects.get(id=group_id)
    if request.method == 'GET':
        requestform = ClientRequestForm(request.GET or None)
    elif request.method == 'POST':
        requestform = StudentGroupModelForm(request.POST)
        if requestform.is_valid():
            requestform.client = request.user.client
            requestform.group = group 
            requestform.save()
        return redirect("client_view_requests")
    context = {'group':group,'form':requestform} 
    return render(request,"client/client_request_group.html",context)

def client_view_requests(request):
    groups = StudentGroup.objects.get(client=request.user.client)
    context = {'groups':groups,'form':form} 
    return render(request,"client/client_view_request.html",context)

def client_view_group_details(request,group_id):
    group = StudentGroup.objects.get(id=group_id)
    context = {'group':group,'form':form} 
    return render(request,"client/client_view_group_details.html",context)

class AddProjectView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "client/add_project.html"

    def form_valid(self,form):
        project = form.save()
        return project 

