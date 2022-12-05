from rest_framework import serializers

import api.models as models


class TMParticipantSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TMParticipant
        fields = '__all__'
