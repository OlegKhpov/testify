from rest_framework import serializers
from testify.models import Test


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = (
            'id',
            'name',
            'description',
            'difficulty'
        )
