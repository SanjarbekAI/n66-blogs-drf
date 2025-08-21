from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.blogs.models import BlogModel
from apps.blogs.serializers import BlogSerializer


@api_view(['GET', 'POST'])
def blog_list_create(request):
    if request.method == "GET":
        blogs = BlogModel.objects.all().order_by('-id')
        serializer = BlogSerializer(blogs, many=True)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    else:
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response({
                "message": "Something went wrong",
            }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def blog_detail(request, pk):
    try:
        blog = BlogModel.objects.get(pk=pk)
    except BlogModel.DoesNotExist:
        return Response({
            "message": "Object does not exists"
        }, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = BlogSerializer(blog)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    elif request.method == "PUT":
        serializer = BlogSerializer(instance=blog, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_202_ACCEPTED
            )
        else:
            return Response({
                "message": "Something went wrong",
            }, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PATCH":
        serializer = BlogSerializer(
            instance=blog, data=request.data, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_202_ACCEPTED
            )
        else:
            return Response({
                "message": "Something went wrong",
            }, status=status.HTTP_400_BAD_REQUEST)

    else:
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
