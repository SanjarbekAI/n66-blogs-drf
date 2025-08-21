from django.urls import path

from apps.blogs.views import blog_list_create

app_name = 'blogs'

urlpatterns = [
    path('', blog_list_create, name='list-create')
]
