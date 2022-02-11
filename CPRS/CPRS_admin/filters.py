import django_filters

from.models import *

class StudentFilter(django_filters.FilterSet):
    class Meta:
        model = Student
        fields = '__all__'

class ProjectFilter(django_filters.FilterSet):
    class Meta:
        model = Project
        exclude = ["file","client"]

class ClientFilter(django_filters.FilterSet):
    class Meta:
        model = Client
        exclude = []
        
class SupervisorFilter(django_filters.FilterSet):
    class Meta:
        model = Supervisor
        exclude = []
class GroupFilter(django_filters.FilterSet):
    class Meta:
        model = StudentGroup
        exclude = ["client"]

class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        exclude = ["description","project","group"]
