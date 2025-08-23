from django.urls import path

from apps.blogs.views import category_list_create, blog_list_create, blog_detail

app_name = 'blogs'

urlpatterns = [
    path('', blog_list_create),
    path('<int:pk>/', blog_detail),
    path('category/', category_list_create),
]
