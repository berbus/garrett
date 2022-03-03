import uuid

from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

import api.models as models
import api.serializers as serializers


class FindingViewSet(viewsets.ModelViewSet):
    queryset = models.Finding.objects.all()
    serializer_class = serializers.FindingSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action in ('list', 'retrieve'):
            permission_classes = (IsAuthenticated, )
        return [permission() for permission in permission_classes]

    def list(self, request, pk=None):
        exercise_id = request.query_params.get('exercise')
        queryset = self.get_queryset()

        if exercise_id:
            try:
                uuid_obj = uuid.UUID(exercise_id)
            except ValueError:
                print(f'Bad value for exercise ID')
                return Response(status=status.HTTP_400_BAD_REQUEST)
            queryset = models.Finding.objects.filter(
                exercise=exercise_id).order_by('creation_date')

        serializer = self.get_serializer(queryset, many=True)
        response_data = serializer.data

        return Response(response_data)
