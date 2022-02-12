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
from django.urls import path, include, re_path
from CPRS_admin.views import *
from CPRS_admin.HOD_views import *
from CPRS_admin.ClientViews import *
from CPRS_admin.SupervisorViews import *
from CPRS_admin.StudentViews import *
from recommendation_system.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    # general urls
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    re_path(r"^download/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(
        r"^student-autocomplete/$",
        StudentNameAutocomplete.as_view(),
        name="student_autocomplete",
    ),
    path("login/", LoginFormView, name="login"),
    path("logout/", Logout, name="logout"),
    path(
        "accounts/signup/student/", StudentSignUpView.as_view(), name="student_signup"
    ),
    path("accounts/signup/client/", ClientSignUpView.as_view(), name="client_signup"),
    path(
        "accounts/signup/supervisor/",
        SupervisorSignUpView.as_view(),
        name="supervisor_signup",
    ),
    # coordinator urls
    path("coordinator/dashboard", admin_dashboard, name="coordinator_dashboard"),
    path("coordinator/search", search, name="search_page"),
    path("", main_view, name="main"),
    path(
        "coordinator/student_list", student_view_list, name="coordinator_view_students"
    ),
    path(
        "coordinator/supervisor_list",
        supervisorview_list,
        name="coordinator_view_supervisors",
    ),
    path("coordinator/project_list", project, name="coordinator_view_projects"),
    path("coordinator/client_list", clientview_list, name="coordinator_view_clients"),
    path(
        "coordinator/student_deactivate/<str:student_id>",
        student_deactivate,
        name="coordinator_deactivate_student",
    ),
    path(
        "coordinator/student_activate/<str:student_id>",
        student_activate,
        name="coordinator_activate_student",
    ),
    path(
        "coordinator/client_deactivate/<str:client_id>",
        client_deactivate,
        name="coordinator_deactivate_client",
    ),
    path(
        "coordinator/client_activate/<str:client_id>",
        client_activate,
        name="coordinator_activate_client",
    ),
    path(
        "coordinator/supervisor_deactivate/<str:supervisor_id>",
        supervisor_deactivate,
        name="coordinator_deactviate_supervisor",
    ),
    path(
        "coordinator/supervisor_activate/<str:supervisor_id>",
        supervisor_activate,
        name="coordinator_activate_supervisor",
    ),
    path(
        "coordinator/view_group_recommendations/<str:group_id>",
        make_recommendations_view,
        name="coordinator_view_project_recommendations",
    ),
    path(
        "coordinator/create_group_with_students",
        create_group_with_students,
        name="coordinator_create_group_with_students",
    ),
    path(
        "coordinator/view_pending_client_requests",
        admin_view_pending_client_requests,
        name="coordinator_view_pending_client_requests",
    ),
    path(
        "coordinator/approve_client_requests/<str:request_id>/<str:group_id>",
        approve_client_request,
        name="approve_client_request",
    ),
    path(
        "coordinator/disapprove_client_request/<str:request_id>/<str:group_id>",
        disapprove_client_request,
        name="disapprove_client_request",
    ),
    path(
        "coordinator/view_group_list/",
        view_group_list,
        name="coordinator_view_groups",
    ),
    path(
        "coordinator/assign_supervisor/<str:group_id>",
        AssignSupervisor,
        name="coordinator_assign_supervisor",
    ),
    path(
        "coordinator/assign_recommended_project/<str:group_id>/<str:client_id>/<str:project_id>",
        assign_recommended_project,
        name="coordinator_assign_project_recommendations",
    ),
    # student urls
    path("accounts/profile/student", student_dashboard, name="student_dashboard"),
    path("student/profile/view", StudentProfile, name="student_view_profile"),
    path(
        "student/profile/edit",
        StudentProfileView.as_view(),
        name="student_edit_profile",
    ),
    path(
        "student/group/details",
        student_view_group_details,
        name="student_view_group_details",
    ),
    path(
        "student/project/details",
        student_view_project_details,
        name="student_view_project_details",
    ),
    path("student/add_task", create_task, name="student_add_task"),
    path(
        "student/update_task_status/<str:task_id>",
        update_task,
        name="student_update_task",
    ),
    path(
        "student/student_view_task_list",
        student_view_task_list,
        name="student_view_task_list",
    ),
    path(
            "student/reply_feedback/<str:feedback_id>",
        student_reply_feedback,
        name="student_reply_feedback",
    ),
    path(
            "student/view_feedback_history",
        student_view_feedback_history,
        name="student_view_feedback_history",
    ),
    # client urls
    path("accounts/profile/client", client_dashboard, name="client_dashboard"),
    path("client/view_projects", client_view_projects, name="client_view_projects"),
    path("client/view_groups", client_view_groups, name="client_view_groups"),
    path("client/view_profile", client_view_profile, name="client_view_profile"),
    path("client/edit_profile", client_edit_profile, name="client_edit_profile"),
    path("client/addproject", add_project_view, name="client_add_project"),
    path(
        "client/request_group_details/<str:group_id>",
        client_request_group,
        name="client_request_group_details",
    ),
    path("client/view_groups", client_view_groups, name="client_view_groups"),
    path("client/view_profile", client_view_profile, name="client_view_profile"),
    path("client/edit_profile", client_edit_profile, name="client_edit_profile"),
    path(
        "client/view_group_details/<str:group_id>",
        client_view_group_details,
        name="client_view_group_details",
    ),
    # supervisor urls
    path(
        "accounts/profile/supervisor", supervisor_dashboard, name="supervisor_dashboard"
    ),
    path(
        "supervisor/view_profile",
        supervisor_view_profile,
        name="supervisor_view_profile",
    ),
    path(
        "supervisor/edit_profile",
        SupervisorProfileEditView.as_view(),
        name="supervisor_edit_profile",
    ),
    path(
        "supervisor/view_groups", supervisor_view_groups, name="supervisor_view_groups"
    ),
    path(
        "supervisor/view_group_details/<str:group_id>",
        supervisor_view_group_details,
        name="supervisor_view_group_details",
    ),
    path(
        "supervisor/view_group_progress/<str:group_id>",
        supervisor_view_group_progress,
        name="supervisor_view_group_progress",
    ),
    path(
        "supervisor/give_feedback/<str:task_id>",
        supervisor_gives_feedback,
        name="supervisor_gives_feedback",
    ),
    path(
        "supervisor/view_feedback_history",
        supervisor_view_feedback_history,
        name="supervisor_view_feedback_history",
    ),
    path(
            "supervisor/archive_feedback/<str:feedback_id>",
        supervisor_archive_feedback,
        name="supervisor_archive_feedback",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
