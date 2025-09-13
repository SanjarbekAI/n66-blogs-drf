from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from apps.blogs.models import BlogPost, Category
from apps.blogs.serializers import BlogPostSerializer, CategorySerializer
from apps.blogs.utils import CustomPageNumberPagination, BlogFilter, BlogCategoryQuery
from apps.shared.utils.custom_response import CustomResponse


class BlogListCreateAPIView(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAdminUser]
    pagination_class = CustomPageNumberPagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_data = self.get_paginated_response(serializer.data)

            return CustomResponse.success(
                message_key="SUCCESS",
                request=request,
                data=paginated_data['results'],
                pagination=paginated_data['pagination']
            )

        return CustomResponse.error(
            message_key='PAGE_NOT_FOUND',
            request=request
        )


class CategoryCreateAPIView(CreateAPIView):
    queryset = Category
    serializer_class = CategorySerializer


class UserBlogListAPIView(ListAPIView):
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, BlogCategoryQuery]
    filterset_class = BlogFilter

    def get_queryset(self):
        queryset = BlogPost.objects.filter(author=self.request.user).order_by('-id')
        return queryset
