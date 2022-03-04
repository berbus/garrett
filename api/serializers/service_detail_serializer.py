from rest_framework import serializers

import api.models as models

from .exercise_serializer import ExerciseSerializer


class ServiceDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Service
        fields = '__all__'

    exercises = serializers.SerializerMethodField()

    def get_exercises(self, service):
        exercises = models.Exercise.objects.filter(service=service).order_by('-creation_date')
        return ExerciseSerializer(exercises, many=True).data
