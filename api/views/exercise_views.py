from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser

import api.models as models
import api.serializers as serializers
import api.services as services


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = models.Exercise.objects.all()
    serializer_class = serializers.ExerciseSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action in ('list', 'retrieve'):
            permission_classes = (IsAuthenticated, )
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        template = serializer.validated_data.get('template')
        exercise = serializer.save()

        for req in template.requirements.all():
            tc = models.TestCase(exercise=exercise, requirement=req)
            tc.save()

        response_data = serializer.data
        response_data['service_name'] = exercise.service.name
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        exercise = get_object_or_404(self.get_queryset(), pk=pk)
        serializerClass = self.get_serializer_class()
        serializer = serializerClass(exercise)
        response_data = serializer.data

        if request.query_params.get('readable'):
            service = models.Service.objects.get(pk=response_data['service'])
            response_data['service_name'] = service.name

        return Response(response_data)
