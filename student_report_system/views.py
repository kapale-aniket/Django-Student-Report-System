"""
Error handler views for custom error pages
"""
from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponseNotFound, HttpResponseServerError


def error_404_view(request, exception):
    """Custom 404 error page handler"""
    return render(request, 'errors/404.html', status=404)


def error_403_view(request, exception):
    """Custom 403 error page handler"""
    return render(request, 'errors/403.html', status=403)


def error_500_view(request):
    """Custom 500 error page handler"""
    return render(request, 'errors/500.html', status=500)







