from rest_framework import serializers

import api.models as models


class ExerciseDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Exercise
        fields = '__all__'

    service_name = serializers.SerializerMethodField()
    template_name = serializers.SerializerMethodField()

    def get_service_name(self, exercise):
        return exercise.service.name

    def get_template_name(self, exercise):
        return exercise.template.name
