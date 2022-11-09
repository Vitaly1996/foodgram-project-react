from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework.pagination import PageNumberPagination

from users.serializers import UserSerializer


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    Вьюсет кастомной модели User
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
