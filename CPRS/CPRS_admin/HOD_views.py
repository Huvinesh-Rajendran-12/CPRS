import json
import requests
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .forms import StudentFormset, StudentGroupModelForm, AssignSupervisorForm
from .models import (
    Recommended_Project,
    Project,
    Student,
    Student_Profile,
    StudentGroup,
    Client,
    Supervisor,
    Client_Request,
)
from .decorators import admin_required
from .filters import (
    StudentFilter,
    ProjectFilter,
    ClientFilter,
    SupervisorFilter,
    GroupFilter,
)

# the dashboard of the admin
@admin_required
def admin_dashboard(request):
    student_count = Student.objects.all().count()
    student_without_group_count = Student.objects.filter(has_group=False).count()
    group_count = StudentGroup.objects.all().count()
    Supervisor_count = Supervisor.objects.all().count()
    project_count = Project.objects.all().count()
    pending_project_count = Project.objects.filter(is_assigned=False).count()
    client_count = Client.objects.all().count()
    requests = Client_Request.objects.filter(approval_status=0)
    context = {
        "student_count": student_count,
        "Supervisor_count": Supervisor_count,
        "project_count": project_count,
        "client_count": client_count,
        "group_count": group_count,
        "student_without_group_count": student_without_group_count,
        "pending_project_count": pending_project_count,
        "requests": requests,
    }
    return render(request, "HOD/dashboard.html", context)


@admin_required
def search(request):
    return render(request, "HOD/search.html")


# view the list of the projects
@admin_required
def project(request):
    projects = Project.objects.all()
    project_filter = ProjectFilter(request.GET, queryset=projects)
    context = {"projects": projects, "project_filter": project_filter}
    return render(request, "HOD/projects.html", context)


# view the recommendations
@admin_required
def recommendations_view(request):
    recommendations = Recommended_Project.objects.filter(is_approved=0)
    return render(request, "HOD/student_leave_view.html", {"leaves": leaves})


@admin_required
def recommendations_approve_view(request, recommendation_id):
    recommendations = Recommended_Project.objects.get(id=recommendation_id)
    recommendations.is_approved = 1
    recommendations.save()
    return HttpResponseRedirect(reverse("recommendations_view"))


@admin_required
def recommendations_disapprove_view(request, recommendation_id):
    recommendations = Recommended_Project.objects.get(id=leave_id)
    recommendations.is_approved = 2

    recommendations.save()
    return HttpResponseRedirect(reverse("recommendations_view"))


# views the list of students
@admin_required
def student_view_list(request):
    students = Student.objects.all()
    student_filter = StudentFilter(request.GET, queryset=students)
    context = {"students": students, "student_filter": student_filter}
    return render(request, "HOD/students.html", context)


# view the list of the clients
@admin_required
def clientview_list(request):
    clients = Client.objects.all()
    client_filter = ClientFilter(request.GET, queryset=clients)
    context = {"clients": clients, "client_filter": client_filter}
    return render(request, "HOD/client_list.html", context)


# view the list of the supervisors
@admin_required
def supervisorview_list(request):
    supervisors = Supervisor.objects.all()
    supervisor_filter = SupervisorFilter(request.GET, queryset=supervisors)
    context = {"supervisors": supervisors, "supervisor_filter": supervisor_filter}
    return render(request, "HOD/supervisors.html", context)


# activate or deactivate the students
@admin_required
def student_deactivate(request, student_id):
    student = Student.objects.get(id=student_id)
    student.is_active = 0
    student.save()
    return redirect(reverse("coordinator_view_students"))


@admin_required
def student_activate(request, student_id):
    student = Student.objects.get(id=student_id)
    student.is_active = 1
    student.save()
    return redirect(reverse("coordinator_view_students"))


# activate or deactivate the clients
@admin_required
def client_deactivate(request, client_id):
    client = Client.objects.get(id=client_id)
    client.is_active = 0
    client.save()
    return redirect(reverse("coordinator_view_clients"))


@admin_required
def client_activate(request, client_id):
    client = Client.objects.get(id=client_id)
    client.is_active = 1
    client.save()
    return redirect(reverse("coordinator_views_clients"))


# activate or deactivate supervisors
@admin_required
def supervisor_deactivate(request, supervisor_id):
    supervisor = Supervisor.objects.get(id=supervisor_id)
    supervisor.is_active = 0
    supervisor.save()
    return redirect(reverse("coordinator_views_supervisors"))


@admin_required
def supervisor_activate(request, supervisor_id):
    supervisor = Supervisor.objects.get(id=supervisor_id)
    supervisor.is_active = 1
    supervisor.save()
    return redirect(reverse("coordinator_views_supervisors"))


# view requests
@admin_required
def admin_view_pending_client_requests(request):
    requests = Client_Request.objects.get(approval_status=0)
    context = {"requests": requests}
    return render(request, "HOD/view_pending_client_requests.html", context)


@admin_required
def admin_view_all_client_requests(request):
    requests = Client_Request.objects.all()
    context = {"requests": requests}
    return render(request, "HOD/view_all_client_requests.html", context)


# approve or disapprove client requests
@admin_required
def disapprove_client_request(request, request_id, group_id):
    group = StudentGroup.objects.get(id=group_id)
    group.can_view = 2
    group.save()
    request = Client_Request.objects.get(id=request_id)
    request.approval_status = 2
    request.save()
    return redirect(reverse("coordinator_dashboard"))


@admin_required
def approve_client_request(request, request_id, group_id):
    group = StudentGroup.objects.get(id=group_id)
    group.can_view = 1
    group.save()
    request = Client_Request.objects.get(id=request_id)
    request.approval_status = 1
    request.save()
    return redirect(reverse("coordinator_dashboard"))


@admin_required
def create_group_with_students(request):
    template_name = "HOD/create_group_with_student.html"
    heading = "Create Student Group"
    students_valid = True
    if request.method == "GET":
        groupform = StudentGroupModelForm(request.GET or None)
        formset = StudentFormset(queryset=Student.objects.none())
    elif request.method == "POST":
        groupform = StudentGroupModelForm(request.POST)
        formset = StudentFormset(request.POST)
        if groupform.is_valid() and formset.is_valid():
            # first save this book, as its reference will be used in `Author`
            for form in formset:
                # so that `book` instance can be attached.
                name = form.cleaned_data.get("name")
                students = Student.objects.filter(name=name).count()
                if students == 0:
                    return HttpResponse("The student " + name + " does not exist")
                student = Student.objects.get(name=name)
                if student.has_group:
                    return HttpResponse("The student " + name + " has a group")
                    students_valid = False
            if students_valid:
                group = groupform.save()
                for form in formset:
                    name = form.cleaned_data.get("name")
                    student = Student.objects.get(name=name)
                    student_profile = Student_Profile.objects.get(student=student)
                    print(student)
                    student_profile.group = group
                    student.group = group
                    student.has_group = True
                    student_profile.save()
                    student.save()
                return redirect("coordinator_dashboard")
        else:
            print("Error...")
    return render(
        request,
        template_name,
        {
            "heading": heading,
            "groupform": groupform,
            "formset": formset,
        },
    )


@admin_required
def view_group_list(request):
    template_name = "HOD/view_group.html"
    groups = StudentGroup.objects.all()
    group_filter = GroupFilter(request.GET, queryset=groups)
    context = {"groups": groups, "group_filter": group_filter}
    return render(request, template_name, context)


@admin_required
def AssignSupervisor(request, group_id):
    """logged in student can create task"""
    template_name = "HOD/assign_supervisor.html"
    group = StudentGroup.objects.get(id=group_id)
    if request.method == "GET":
        assignsupervisorform = AssignSupervisorForm(request.GET or None)
    elif request.method == "POST":
        assignsupervisorform = AssignSupervisorForm(request.POST)
        if assignsupervisorform.is_valid():
            group.supervisor = assignsupervisorform.cleaned_data.get("supervisor")
            group.save()
        return redirect("coordinator_view_groups")
    context = {"form": assignsupervisorform}
    return render(request, template_name, context)
