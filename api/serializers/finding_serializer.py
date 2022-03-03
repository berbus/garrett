
from rest_framework import serializers

import api.models as models


class FindingSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Finding
        fields = '__all__'
