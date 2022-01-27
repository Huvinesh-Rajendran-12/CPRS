import json

import requests
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import Recommended_Project , Project
def admin_dashboard(request):
    requests = Request.objects.filter(is_approved=0)
    context = {'requests':request}
    return render(request, "HOD/dashboard.html",context)

def search(request):
    return render(request, "HOD/search.html")

def project(request):
    projects = Project.objects.alll()
    context = {'projects':projects}
    return render(request, "HOD/projects.html",context)
a
def recommendations_view(request):
    recommendations= Recommended_Project.objects.filter(is_approved=0)
    return render(request,"hod_template/student_leave_view.html",{"leaves":leaves})


def recommendations_approve_view(request,recommendation_id):
    recommendations=Recommended_Project.objects.get(id=recommendation_id)
    recommendations.is_approved=1
    recommendations.save()
    return HttpResponseRedirect(reverse("recommendations_view"))

def recommendations_disapprove_view(request,recommendation_id):
    recommendations = Recommended_Project.objects.get(id=leave_id)
    recommendations.is_approved=2

    recommendations.save()
    return HttpResponseRedirect(reverse("recommendations_view"))


