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

urlpatterns = [
    path("admin/", admin.site.urls),
    path("home/", home_view, name="home"),
    path("student/", student_view, name="student"),
    path("group/", group_view, name="group"),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
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
]
