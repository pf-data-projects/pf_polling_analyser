from django.shortcuts import render
from django.core.exceptions import PermissionDenied


def handler500(request):
    """Renders the 500 page when error occurs"""
    return render(request, '500.html', status=500)


def handler404(request, exception):
    """Renders the 404 page"""
    return render(request, '404.html', status=404)
