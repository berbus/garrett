from rest_framework import serializers

import api.models as models


class ThreatModelDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ThreatModel
        fields = '__all__'

    services = serializers.SerializerMethodField(read_only=True)
    review = serializers.SerializerMethodField(read_only=True)

    def get_services(self, threat_model):
        res = []
        for service in threat_model.services.all():
            res.append({'name': service.name, 'oid': service.oid})
        return res

    def get_review(self, threat_model):
        if threat_model.review is None:
            res = None
        else:
            res = {'title': threat_model.review.title, 'oid': threat_model.review.oid}
        return res
