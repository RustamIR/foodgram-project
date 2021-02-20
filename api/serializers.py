from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from api.models import Favorite, Purchase, Subscribe
from recipes.models import Ingredient, Recipe

User = get_user_model()


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.SlugRelatedField(
        slug_field='id', queryset=Recipe.objects.all(), source='recipe'
    )
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ['id', 'user']
        model = Favorite
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(), fields=['id', 'user']
            )
        ]

    def validate(self, attrs):
        user = self.context['request'].user
        if user == attrs['recipe'].author:
            raise ValidationError(
                'Нельзя добавить в избранное свой собственный рецепт'
            )
        return attrs

    def create(self, validated_data):
        if 'user' not in validated_data:
            validated_data['user'] = self.context['request'].user
        return Favorite.objects.create(**validated_data)


class PurchaseSerializer(serializers.ModelSerializer):
    id = serializers.SlugRelatedField(
        slug_field='id', queryset=Recipe.objects.all(), source='recipe'
    )
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ['id', 'user']
        model = Purchase
        validators = [
            UniqueTogetherValidator(
                queryset=Purchase.objects.all(), fields=['id', 'user']
            )
        ]

    def create(self, validated_data):
        if 'user' not in validated_data:
            validated_data['user'] = self.context['request'].user
        return Purchase.objects.create(**validated_data)


class SubscribeSerializer(serializers.ModelSerializer):
    id = serializers.SlugRelatedField(
        slug_field='id', queryset=User.objects.all(), source='author'
    )
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ['id', 'user']
        model = Subscribe
        validators = [
            UniqueTogetherValidator(
                queryset=Subscribe.objects.all(), fields=['id', 'user']
            )
        ]

    def validate(self, attrs):
        user = self.context['request'].user
        if user == attrs['author']:
            raise ValidationError('Нельзя подписаться на себя')
        return attrs

    def create(self, validated_data):
        if 'user' not in validated_data:
            validated_data['user'] = self.context['request'].user
        return Subscribe.objects.create(**validated_data)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredient

#
# from rest_framework import serializers
# from rest_framework.exceptions import ValidationError
#
#
# from recipes.models import Ingredient
# from .models import Subscribe, Favorite, Purchase
#
#
# class CustomModelSerializer(serializers.ModelSerializer):
#     def create(self, validated_data):
#         validated_data['user'] = self.context['request'].user
#         return self.Meta.model.objects.create(**validated_data)
#
#
# class IngredientSerializer(serializers.ModelSerializer):
#     class Meta:
#         fields = ('title', 'dimension')
#         model = Ingredient
#
#
# class SubscriptionSerializer(CustomModelSerializer):
#     class Meta:
#         fields = ('author', )
#         model = Subscribe
#
#     def validate_author(self, value):
#         user = self.context['request'].user
#         if user.id == value:
#             raise ValidationError('Нельзя подписаться на самого себя')
#         return value
#
#
# class FavoriteSerializer(CustomModelSerializer):
#     class Meta:
#         fields = ('recipe', )
#         model = Favorite
#
#
# class PurchaseSerializer(CustomModelSerializer):
#     class Meta:
#         fields = ('recipe', )
#         model = Purchase