from django.urls import path

from apps.accounts.views import RegisterCreateAPIView, LoginAPIView

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterCreateAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
]
