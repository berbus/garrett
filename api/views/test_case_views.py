import uuid

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import api.models as models
import api.serializers as serializers


class TestCaseViewSet(viewsets.ModelViewSet):
    queryset = models.TestCase.objects.all()
    serializer_class = serializers.TestCaseSerializer
    permission_classes = (IsAuthenticated, )

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
                _ = uuid.UUID(exercise_id)
            except ValueError:
                print('Bad value for exercise ID')
                return Response(status=status.HTTP_400_BAD_REQUEST)
            queryset = models.TestCase.objects.filter(exercise=exercise_id).order_by(
                'requirement__owasp_section', 'requirement__readable_id')

        serializer = self.get_serializer(queryset, many=True)
        response_data = serializer.data

        return Response(response_data)

    @action(methods=['PATCH'], detail=False)
    def bulk_update(self, request):
        test_ids = request.data.get('test_ids')
        new_data = request.data.get('new_data')

        # TODO - Is unsanitised data bad?
        queryset = self.get_queryset().filter(pk__in=test_ids)
        queryset.update(**new_data)
        response_data = self.get_serializer(queryset, many=True).data

        return Response(response_data)
