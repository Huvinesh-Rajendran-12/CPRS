import json

import requests
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .forms import GroupForm , StudentFormset

from .models import Recommended_Project , Project , Student , StudentGroup, Client
def admin_dashboard(request):
    requests = Request.objects.filter(is_approved=0)
    context = {'requests':request}
    return render(request, "HOD/dashboard.html",context)

def search(request):
    return render(request, "HOD/search.html")

def project(request):
    projects = Project.objects.all()
    context = {'projects':projects}
    return render(request, "HOD/projects.html",context)

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

def student_view_list(request):
    students = Student.objects.all()
    context = {'students':students}
    return render(request,"HOD/students.html",context)

def add_student_group(request):
    if request.POST:
        form = GroupForm(request.POST)
        form.student_instances = StudentFormset(request.POST)
        if form.is_valid():
            group = StudentGroup()

            group.name= form.cleaned_data['name']
            group.save()

        if form.student_instances.cleaned_data is not None:

            for item in form.student_instances.cleaned_data:
                student = Student.objects.filter(id=item['id'])
                player.pname= item['pname']
                player.hscore= item['hscore']
                player.age= item['age']
                player.save()
                group.student.add(student)
            group.save()

    else:
        form = GroupForm()
        return render(request, 'HOD/add_student_group.html', {'form':form})

def clientview_list(request):
    clients = Client.objects.all()
    context = {'clients':clients}
    return render(request,"HOD/client_list.html",context)

