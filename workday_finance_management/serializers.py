from rest_framework import serializers
from .models import Operation, Journal


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = "__all__"


class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = "__all__"
