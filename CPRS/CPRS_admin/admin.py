from django.contrib import admin
from .models import Student, StudentGroup, Client, Supervisor, User, Project
from django.contrib.auth.models import Group
from .forms import GroupAdminForm, StudentGroupAdminForm

# Register your models here.


class StudentAdmin(admin.ModelAdmin):
    search_fields = ["id"]


class SupervisorAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "first_name", "last_name"]
    search_fields = ["id", "email"]


class ClientAdmin(admin.ModelAdmin):
    list_display = ["id", "company"]
    search_fields = ["id", "company"]


class UserAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name"]
    search_fields = ["first_name", "last_name"]


class ProjectAdmin(admin.ModelAdmin):
    list_display = ["title", "overview"]
    search_fields = ["title", "overview"]


class GroupAdmin(admin.ModelAdmin):
    # Use our custom form.
    form = GroupAdminForm
    # Filter permissions horizontal as well.
    filter_horizontal = ["permissions"]


class StudentGroupAdmin(admin.ModelAdmin):
    form = StudentGroupAdminForm


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Supervisor, SupervisorAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(StudentGroup, StudentGroupAdmin)
