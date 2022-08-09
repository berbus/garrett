from rest_framework import serializers

import api.models as models


class ThreatModelDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ThreatModel
        fields = '__all__'

    service = serializers.SerializerMethodField(read_only=True)
    review = serializers.SerializerMethodField(read_only=True)

    def get_service(self, threat_model):
        return {'name': threat_model.service.name, 'oid': threat_model.service.oid}

    def get_review(self, threat_model):
        if threat_model.review is None:
            res = None
        else:
            res = {'title': threat_model.review.title, 'oid': threat_model.review.oid}
        return res
