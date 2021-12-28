# from django.contrib.auth.models import User
from .models import User

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """ A serializer class for the User model """
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email',
                  'is_admin', 'is_active', 'is_superuser')
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)