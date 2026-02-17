"""
Middleware to add no-cache headers to prevent browser caching
"""
from django.utils.cache import add_never_cache_headers
from django.http import HttpResponse


class NoCacheMiddleware:
    """
    Middleware to prevent browser caching of pages.
    This ensures users always see fresh content after logout.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Don't add no-cache headers to static files, media files, or API responses
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            return response
        
        # For HTML responses, add no-cache headers
        if hasattr(response, 'content_type') and 'text/html' in response.get('Content-Type', ''):
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        
        return response


