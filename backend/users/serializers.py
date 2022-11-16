from api.serializers import *
from django.contrib.auth import get_user_model
from rest_framework import serializers
from recipes.models import Recipe

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers. SerializerMethodField()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return request.user.follower.filter(author=obj).exists()

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


class FollowListSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField('recipes_limit')
    recipes_count = serializers.SerializerMethodField()

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

    class Meta:
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
