from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET', 'POST'])
def blog_list_create(request):
    return Response({
        "message": "ok"
    })
