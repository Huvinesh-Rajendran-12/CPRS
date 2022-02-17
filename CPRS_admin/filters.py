import django_filters

from .models import *


class StudentFilter(django_filters.FilterSet):
    class Meta:
        model = Student
        exclude = ["user"]


class ProjectFilter(django_filters.FilterSet):
    class Meta:
        model = Project
        exclude = ["file"]

class ClientProjectFilter(django_filters.FilterSet):
    class Meta:
        model = Project
        exclude = ["client","file"]

class ClientFilter(django_filters.FilterSet):
    class Meta:
        model = Client
        exclude = ["user"]


class SupervisorFilter(django_filters.FilterSet):
    class Meta:
        model = Supervisor
        exclude = ["user"]


class GroupFilter(django_filters.FilterSet):
    class Meta:
        model = StudentGroup
        exclude = ["can_view","has_requested"]


class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        exclude = ["description", "project", "group", "created_by", "assigned_to"]
