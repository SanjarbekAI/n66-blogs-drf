import base64
from functools import wraps

import django_filters
from django.contrib.auth import authenticate
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from rest_framework import filters
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from apps.blogs.models import BlogPost


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


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 10

    def __init__(self):
        super().__init__()
        self.page = None
        self.request = None

    def paginate_queryset(self, queryset, request, view=None):
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = Paginator(queryset, page_size)
        page_number = request.query_params.get(self.page_query_param, 1)

        try:
            self.page = paginator.page(page_number)
        except (PageNotAnInteger, EmptyPage):
            return None

        self.request = request
        return list(self.page)

    def get_paginated_response(self, data):
        if self.page is None:
            return {
                'pagination': {
                    'total_items': 0,
                    'total_pages': 0,
                    'current_page': 0,
                    'page_size': 0,
                    'next_page': None,
                    'prev_page': None,
                },
                'results': None
            }

        return {
            'pagination': {
                'total_items': self.page.paginator.count,
                'total_pages': self.page.paginator.num_pages,
                'current_page': self.page.number,
                'page_size': len(data),
                'next_page': self.page.next_page_number() if self.page.has_next() else None,
                'prev_page': self.page.previous_page_number() if self.page.has_previous() else None,
            },
            'results': data
        }


class BlogCategoryQuery(filters.SearchFilter):
    def get_schema_operation_parameters(self, view):
        return [
            {
                'name': 'cat',
                'required': False,
                'in': 'query',
                'description': 'Category id',
                'schema': {
                    'type': 'int',
                },
            }
        ]


class BlogFilter(django_filters.FilterSet):
    cat = django_filters.NumberFilter(field_name='category_id')

    class Meta:
        model = BlogPost
        fields = ['cat']
