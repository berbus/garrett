from rest_framework import serializers

import api.models as models

from .exercise_detail_serializer import ExerciseDetailSerializer


class ServiceDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Service
        fields = '__all__'

    exercises = serializers.SerializerMethodField()

    def get_exercises(self, service):
        res = []
        exercises = models.Exercise.objects.filter(service=service).order_by('-creation_date')
        for exercise in exercises:
            res.append(ExerciseDetailSerializer(exercise).data)

        return res
