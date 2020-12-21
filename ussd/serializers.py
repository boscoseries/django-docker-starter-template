from rest_framework import serializers
from .models import USSD


class USSDSerializer(serializers.ModelSerializer):
    class Meta:
        model = USSD
        fields = '__all__'
