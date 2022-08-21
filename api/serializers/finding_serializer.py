from rest_framework import serializers

import api.models as models


class FindingSerializer(serializers.ModelSerializer):
    test_case_data = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Finding
        fields = '__all__'

    def get_test_case_data(self, finding):
        return {'oid': finding.test_case.oid, 'name': finding.test_case.requirement.readable_id}
