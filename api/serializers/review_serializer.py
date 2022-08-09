from rest_framework import serializers

import api.models as models


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Review
        fields = '__all__'

    service_names = serializers.SerializerMethodField(read_only=True)

    def get_service_names(self, review):
        return {str(service.oid): service.name for service in review.services.all()}
