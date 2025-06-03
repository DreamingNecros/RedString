#facilite la partie transformation en json + permet de valider les donnée
from rest_framework import serializers
from User.models import AuthUser
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = ['username', 'first_name', 'last_name', 'email', 'phone']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'phone']

    def validate_password(self, value):
        return make_password(value)

    def create(self, validated_data):
        validated_data['is_active'] = 1
        validated_data['is_staff'] = 0
        validated_data['is_superuser'] = 0
        return super().create(validated_data)
    
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = ['username', 'first_name', 'last_name', 'email', 'phone']