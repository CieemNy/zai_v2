from rest_framework import serializers
from .models import Film
from django.contrib.auth.models import User


class FilmModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
