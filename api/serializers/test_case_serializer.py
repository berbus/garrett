from rest_framework import serializers

import api.models as models
from .requirement_serializer import RequirementSerializer


class TestCaseSerializer(serializers.ModelSerializer):
    requirement = RequirementSerializer(many=False, read_only=True)

    class Meta:
        model = models.TestCase
        fields = '__all__'
