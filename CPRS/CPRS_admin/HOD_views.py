import json
import requests
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .forms import StudentFormset, StudentGroupModelForm 
from .models import Recommended_Project , Project , Student , StudentGroup, Client, Supervisor, Client_Request


#the dashboard of the admin 
def admin_dashboard(request):
    # requests = Request.objects.filter(is_approved=0)
    context = {'requests':request}
    return render(request, "HOD/dashboard.html")


def search(request):
    return render(request, "HOD/search.html")


#view the list of the projects 
def project(request):
    projects = Project.objects.all()
    context = {'projects':projects}
    return render(request, "HOD/projects.html",context)


#view the recommendations 
def recommendations_view(request):
    recommendations= Recommended_Project.objects.filter(is_approved=0)
    return render(request,"HOD/student_leave_view.html",{"leaves":leaves})


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

#views the list of students 
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

#view the list of the clients 
def clientview_list(request):
    clients = Client.objects.all()
    context = {'clients':clients}
    return render(request,"HOD/client_list.html",context)

#view the list of the supervisors 
def supervisorview_list(request):
    supervisors = Supervisor.objects.all()
    context = {'supervisors':supervisors}
    return render(request,"HOD/supervisors.html",context)


#activate or deactivate the students 
def student_deactivate(request,student_id):
    student=Student.objects.get(id=student_id)
    student.is_active=0
    student.save()
    return redirect(reverse("student_view_list"))
def student_activate(request,student_id):
    student=Student.objects.get(id=student_id)
    student.is_active=1
    student.save()
    return redirect(reverse("student_view_list"))

#activate or deactivate the clients 
def client_deactivate(request,client_id):
    client=Client.objects.get(id=client_id)
    client.is_active=0
    client.save()
    return redirect(reverse("clientview_list"))
def client_activate(request,client_id):
    client=Client.objects.get(id=client_id)
    client.is_active=1
    client.save()
    return redirect(reverse("clientview_list"))

#activate or deactivate supervisors
def supervisor_deactivate(request,supervisor_id):
    supervisor=Supervisor.objects.get(id=supervisor_id)
    supervisor.is_active=0
    supervisor.save()
    return redirect(reverse("supervisorview_list"))

def supervisor_activate(request,supervisor_id):
    supervisor=Supervisor.objects.get(id=supervisor_id)
    supervisor.is_active=1
    supervisor.save()
    return redirect(reverse("supervisorview_list"))

#view requests 
def admin_view_pending_client_requests(request):
    requests = Client_Request.objects.get(approval_status=0)
    context = {'requests':requests}
    return render(request,"HOD/view_pending_client_requests.html",context)

def admin_view_all_client_requests(request):
    requests = Client_Request.objects.all()
    context = {'requests':requests}
    return render(request,"HOD/view_all_client_requests.html",context)


#approve or disapprove client requests 
def disapprove_request(request,request_id):
    request=Client_Request.objects.get(id=request_id)
    request.approval_status=2
    request.save()
    return redirect(reverse("supervisorview_list"))

def approve_request(request,request_id):
    request=Client_Request.objects.get(id=request_id)
    request.approval_status=1
    request.save()
    return redirect(reverse("supervisorview_list"))

def create_group_with_students(request):
    template_name = 'HOD/create_group_with_student.html'
    if request.method == 'GET':
        groupform = StudentGroupModelForm(request.GET or None)
        formset = StudentFormset(queryset=Student.objects.none())
    elif request.method == 'POST':
        groupform = StudentGroupModelForm(request.POST)
        formset = StudentFormset(request.POST)
        if groupform.is_valid() and formset.is_valid():
            # first save this book, as its reference will be used in `Author`
            group = groupform.save()
            for form in formset:
                # so that `book` instance can be attached.
                name = form.cleaned_data.get("name")
                student = Student.objects.get(name=name)
                student.group = group
                student.has_group = True
                student.save()
            return redirect('admin_dashboard')
    return render(request, template_name, {
        'groupform': groupform,
        'formset': formset,
    })


