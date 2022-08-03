from rest_framework import serializers

import api.models as models


class JiraIssueSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.JiraIssue
        fields = '__all__'
