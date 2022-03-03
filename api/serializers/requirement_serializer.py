from rest_framework import serializers

import api.models as models


class RequirementSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Requirement
        fields = ['oid', 'readable_id', 'description', 'owasp_section', 'owasp_level']
