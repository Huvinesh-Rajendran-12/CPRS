from .decorators import supervisor_required
from django.shortcuts import render, redirect


@supervisor_required
def supervisor_dashboard(request):
    template_name = "supervisor/supervisor_dashboard.html"
    return render(request, template_name)
