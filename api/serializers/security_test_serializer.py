from rest_framework import serializers

import api.models as models


class SecurityTestSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SecurityTest
        fields = '__all__'
