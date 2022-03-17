from rest_framework import serializers
from api.models.user import User


class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
