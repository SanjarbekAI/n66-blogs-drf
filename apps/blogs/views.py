from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.blogs.models import BlogPost
from apps.blogs.serializers import CategorySerializer, BlogPostSerializer
from apps.blogs.utils import basic_auth_required


@api_view(['GET', 'POST'])
def category_list_create(request):
    if request.method == "POST":
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
    return None


@api_view(['GET', 'POST'])
@basic_auth_required
def blog_list_create(request):
    if request.method == "POST":
        serializer = BlogPostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        return None
    else:
        blogs = BlogPost.objects.all()
        serializer = BlogPostSerializer(blogs, many=True)
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )


@api_view(['GET', 'PATCH'])
@basic_auth_required
def blog_detail(request, pk):
    blog = BlogPost.objects.get(pk=pk)
    if request.method == "PATCH":
        serializer = BlogPostSerializer(
            data=request.data,
            instance=blog
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
    return None
