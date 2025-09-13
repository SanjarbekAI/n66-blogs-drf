from django.urls import path

from apps.blogs.views import BlogListCreateAPIView, CategoryCreateAPIView, UserBlogListAPIView

app_name = 'blogs'

urlpatterns = [
    path('', BlogListCreateAPIView.as_view()),
    path('me/', UserBlogListAPIView.as_view()),
    path('category/', CategoryCreateAPIView.as_view()),
]
