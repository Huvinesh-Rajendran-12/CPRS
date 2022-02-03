from django.contrib import admin
from .models import Student, StudentGroup, Client, Supervisor, User, Project
from django.contrib.auth.models import Group

# Register your models here.


class StudentAdmin(admin.ModelAdmin):
    list_display = ["id"]
    search_fields = ["id"]


class SupervisorAdmin(admin.ModelAdmin):
    list_display = ["id"]
    search_fields = ["id"]


class ClientAdmin(admin.ModelAdmin):
    list_display = ["id"]
    search_fields = ["id"]


class UserAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name"]
    search_fields = ["first_name", "last_name"]


class ProjectAdmin(admin.ModelAdmin):
    list_display = ["title", "overview"]
    search_fields = ["title", "overview"]


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Supervisor, SupervisorAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Group)
admin.site.register(StudentGroup)
