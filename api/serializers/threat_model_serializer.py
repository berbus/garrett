from rest_framework import serializers

import api.models as models


class ThreatModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ThreatModel
        fields = '__all__'
