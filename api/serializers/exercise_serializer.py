from rest_framework import serializers

import api.models as models


class ExerciseSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Exercise
        fields = '__all__'
