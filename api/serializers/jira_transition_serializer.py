from rest_framework import serializers

import api.models as models


class JiraTransitionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.JiraTransition
        fields = '__all__'
