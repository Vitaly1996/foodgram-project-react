from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.pagination import CustomPagination
from users.serializers import FollowListSerializer
from users.models import Follow


class FollowListViewSet(viewsets.ModelViewSet):
    @action(
            detail=False,
            methods=['GET'],
            permission_classes=[permissions.IsAuthenticated]
        )
    def subscriptions(self, request):
        queryset = User.objects.filter(following__user=self.request.user)
        if queryset:
            pages = self.paginate_queryset(queryset)
            serializer = FollowListSerializer(
                pages,
                many=True,
                context={'request': request})
            return self.get_paginated_response(serializer.data)
        return Response('Вы ни на кого не подписаны',
                        status=status.HTTP_400_BAD_REQUEST
                        )


class FollowViewSet(viewsets.ModelViewSet):
        @action(
            detail=True,
            methods=['POST', 'DELETE'],
            url_path=r'(?P<users>\d+)/subscribe',
            url_name='user_subscribe',
            permission_classes=[permissions.IsAuthenticated]
        )
        def subscribe(self, request, id):
            user = request.user
            author = get_object_or_404(Follow, id=id)
            if request.method == 'POST':
                serializer = FollowSerializer(
                    data={
                        'user': user.id,
                        'author': author.id
                    },
                    context={'request': request}
                )
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        serializer.data, status=status.HTTP_201_CREATED
                    )
            subscription = get_object_or_404(
                Follow,
                user=user,
                author=author
            )
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

#
# User = get_user_model()
#
#
# class UserViewSet(viewsets.ModelViewSet):
#     """
#     Вьюсет кастомной модели User
#     """
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     pagination_class = CustomPagination
#
#     @action(
#         detail=False,
#         methods=['GET'],
#         permission_classes=[permissions.IsAuthenticated]
#     )
#     def subscriptions(self, request):
#         queryset = User.objects.filter(following__user=self.request.user)
#         if queryset:
#             pages = self.paginate_queryset(queryset)
#             serializer = FollowSerializer(
#                 pages,
#                 many=True,
#                 context={'request': request})
#             return self.get_paginated_response(serializer.data)
#         return Response('Вы ни на кого не подписаны',
#                         status=status.HTTP_400_BAD_REQUEST
#                         )
#
#     @action(
#         detail=True,
#         methods=['POST', 'DELETE'],
#         url_path=r'(?P<users>\d+)/subscribe',
#         url_name='user_subscribe',
#         permission_classes=[permissions.IsAuthenticated]
#     )
#     def subscribe(self, request, id):
#         user = request.user
#         author = get_object_or_404(Follow, id=id)
#         if request.method == 'POST':
#             serializer = FollowSerializer(
#                 data={
#                     'user': user.id,
#                     'author': author.id
#                 },
#                 context={'request': request}
#             )
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(
#                     serializer.data, status=status.HTTP_201_CREATED
#                 )
#         subscription = get_object_or_404(
#             Follow,
#             user=user,
#             author=author
#         )
#         subscription.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#         print('Оно работает')



