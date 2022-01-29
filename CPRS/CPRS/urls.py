"""CPRS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from CPRS_admin.views import *
from CPRS_admin.HOD_views import * 

urlpatterns = [
    path("admin/", admin.site.urls),
    path("home/", home_view, name="home"),
    path("student/", student_view, name="student"),
    path("group/", group_view, name="group"),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/login/",signin,name="login"),
    path(
        "accounts/signup/student/", StudentSignUpView.as_view(), name="student_signup"
    ),
    path("accounts/signup/client/", ClientSignUpView.as_view(), name="client_signup"),
    path(
        "accounts/signup/supervisor/",
        SupervisorSignUpView.as_view(),
        name="supervisor_signup",
    ),
    path("coordinator/dashboard", admin_dashboard, name="admin_dashboard"),
    path("coordinator/search", search, name="search_page"),
    path("coordinator/projects", project, name="projects"),
    path("accounts/profile/student", student_dashboard, name="student_dashboard"),
    path("accounts/profile/supervisor", supervisor_dashboard, name="supervisor_dashboard"),
    path("accounts/profile/client", client_dashboard, name="client_dashboard"),
    path("main/",main_view,name="main"),
    path("client/addproject",AddProjectView.as_view(),name="add_project"),
    
    path("coordinator/student_list",student_view_list,name="student_list"),

    path("coordinator/project_list",project,name="project_list"), 

    path("coordinator/add_student_group",add_student_group,name="add_student_group"),
    path("coordinator/client_list",clientview_list,name="client_list"),
    path("student/profile/edit",StudentProfileView.as_view(),name="student_profile_edit"),
    
]
