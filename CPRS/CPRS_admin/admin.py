from django.contrib import admin
from .models import Students, Client, Supervisor, User
# Register your models here.

admin.site.register(User)
admin.site.register(Students)
admin.site.register(Client)
admin.site.register(Supervisor)

