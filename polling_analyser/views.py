""" 
Views to handle overal all application functions

handler500: returns the 500 error page 
and response code if a server error happens

handler404: returns 404 error page
and response code if the user tries to
access a page that doesn't exist.
"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Standard library
from django.shortcuts import render
from django.core.exceptions import PermissionDenied


def handler500(request):
    """Renders the 500 page when error occurs"""
    return render(request, '500.html', status=500)


def handler404(request, exception):
    """Renders the 404 page"""
    return render(request, '404.html', status=404)
