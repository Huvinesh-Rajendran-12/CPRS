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
from CPRS_admin.ClientViews import * 
urlpatterns = [
    path("admin/", admin.site.urls),
    path("home/", home_view, name="home"),
    path("student/", student_view, name="student"),
    path("group/", group_view, name="group"),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("login/",LoginView.as_view(),name="login"),
    path("logout/",Logout,name="logout"),
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
    path("",main_view,name="main"),
    path("client/addproject",AddProjectView.as_view(),name="add_project"),
    
    path("coordinator/student_list",student_view_list,name="student_list"),
    path("coordinator/supervisor_list",supervisorview_list,name="student_list"),

    path("coordinator/project_list",project,name="project_list"), 

    path("coordinator/add_student_group",add_student_group,name="add_student_group"),
    path("coordinator/client_list",clientview_list,name="client_list"),
    path("student/profile/edit",StudentProfileView.as_view(),name="student_profile_edit"),
    path("student_deactivate/<str:student_id>",student_deactivate,name="student_deactivate"),
    path("student_activate/<str:student_id>",student_activate,name="student_activate"),
    path("client_deactivate/<str:client_id>",client_deactivate,name="client_deactivate"),
    path("client_activate/<str:client_id>",client_activate,name="client_activate"),
    path("supervisor_deactivate/<str:supervisor_id>",supervisor_deactivate,name="supervisor_deactivate"),
    path("client_activate/<str:client_id>",supervisor_activate,name="supervisor_activate"),
    path("signup2/",signup2,name="signup2"),
    path("student/profile/view",StudentProfile,name="student_profile_view"),
    path("coordinator/create_group_with_students",create_group_with_students,name="create_group_with_students"),
    path("client/request_group_details/<str:group_id",client_request_group,name="client_request_group_details"),
    path("client/view_group_requests",client_view_requests,name="client_view_requests"),
    path("client/view_group_details/<str:group_id",client_view_group_details,name="client_view_requests"),
    path("coordinator/view_pending_client_requests",admin_view_pending_client_requests,name="view_pending_client_requests"),
    path("coordinator/approve_client_requests/<str:request_id",approve_request,name="approve_request"),
    path("coordinator/disapprove_client_request/<str:request_id",disapprove_request,name="disapprove_request"),
    
]
