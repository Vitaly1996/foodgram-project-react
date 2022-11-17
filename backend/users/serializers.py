from api.serializers import *
from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from recipes.models import Recipe
from rest_framework import serializers
from users.models import Follow

User = get_user_model()


class UsersSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:

        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        user = request.user
        author = obj
        if not request or request.user.is_anonymous:
            return False
        subcribe = Follow.objects.filter(user=user, author=author)
        return subcribe.exists()


class FollowListSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField('recipes_limit')
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes_limit(self, obj):
        request = self.context.get('request')
        recipes_limit = request.query_params.get('recipes_limit')
        if not recipes_limit:
            return RecipeShortInfo(
                Recipe.objects.filter(author=obj),
                many=True,
                context={'request': request}
            ).data
        return RecipeShortInfo(
            Recipe.objects.filter(author=obj)[:int(recipes_limit)],
            many=True,
            context={'request': request}
        ).data


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('author', 'user')

    def to_representation(self, instance):
        request = self.context.get('request')
        return FollowListSerializer(
            instance.author,
            context={'request': request}
        ).data

    def validate(self, data):
        request = self.context.get('request')
        user = request.user
        author = data.get('author')
        if Follow.objects.filter(user=user, author=author):
            raise serializers.ValidationError('Вы уже подписаны.')
        if user == author:
            raise serializers.ValidationError('Вы не можете подписаться на себя')
        return data
