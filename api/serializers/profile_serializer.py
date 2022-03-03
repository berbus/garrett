from rest_framework import serializers

import api.models as models


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Profile
        fields = ('picture',)
