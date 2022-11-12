from rest_framework import viewsets
from django.contrib.auth import get_user_model

from users.serializers import UserSerializer
from api.pagination import CustomPagination

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    Вьюсет кастомной модели User
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination
