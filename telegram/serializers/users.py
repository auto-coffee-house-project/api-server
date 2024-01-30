from rest_framework import serializers

from telegram.models import User

__all__ = ('UserSerializer',)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
