from rest_framework import serializers
from .models import *


class PositionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Positions
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

class AthleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Athlete
        fields = '__all__'

class AnthropometricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anthropometric
        fields = '__all__'