import base64
from functools import wraps

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response


def basic_auth_required(view_func):
    """
    Decorator that requires Basic Authentication (username:password) for every request
    Supports both Authorization header and custom Username/Password headers
    """

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        username = None
        password = None

        # Check for Basic Auth header first
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Basic '):
            try:
                # Decode basic auth
                encoded_credentials = auth_header.split(' ')[1]
                decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
                username, password = decoded_credentials.split(':', 1)
            except (ValueError, IndexError, UnicodeDecodeError):
                return Response({
                    'error': 'Invalid Basic Authorization header format'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # Check for custom headers as fallback
            username = request.META.get('HTTP_USERNAME')
            password = request.META.get('HTTP_PASSWORD')

        if not username or not password:
            return Response({
                'error': 'Basic Authentication required. Send username and password with every request.',
                'auth_methods': [
                    'Authorization: Basic <base64(username:password)>',
                    'Headers: Username and Password'
                ]
            }, status=status.HTTP_401_UNAUTHORIZED)

        # Authenticate user
        user = authenticate(username=username, password=password)
        if not user:
            return Response({
                'error': 'Invalid username or password'
            }, status=status.HTTP_401_UNAUTHORIZED)

        # Add authenticated user to request
        request.user = user
        return view_func(request, *args, **kwargs)

    return wrapper
