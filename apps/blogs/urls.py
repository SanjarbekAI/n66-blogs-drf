from django.urls import path

from apps.blogs.views import blog_list_create, blog_detail

app_name = 'blogs'

urlpatterns = [
    path('<int:pk>/', blog_detail, name='detail'),
    path('', blog_list_create, name='list-create'),
]
