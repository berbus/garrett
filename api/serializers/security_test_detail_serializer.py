from rest_framework import serializers

import api.models as models


class SecurityTestDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SecurityTest
        fields = '__all__'

    service = serializers.SerializerMethodField(read_only=True)
    template = serializers.SerializerMethodField(read_only=True)
    review = serializers.SerializerMethodField(read_only=True)

    def get_service(self, security_test):
        return {'name': security_test.service.name, 'oid': security_test.service.oid}

    def get_template(self, security_test):
        return {'name': security_test.template.name, 'oid': security_test.template.oid}

    def get_review(self, security_test):
        if security_test.review is None:
            res = None
        else:
            res = {'title': security_test.review.title, 'oid': security_test.review.oid}
        return res
