"""
Serializer for recipr API
"""
from rest_framework import serializers

from core.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for Recipe"""

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link']
        read_only = ['id']

class RecipeDetailsSerializer(RecipeSerializer):
    """Serializer for RecipeDetails"""

    class meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']
