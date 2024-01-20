from rest_framework import serializers

from telegram.models import Bot

__all__ = ('BotSerializer',)


class BotSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bot
        fields = '__all__'
