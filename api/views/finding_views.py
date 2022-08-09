import uuid

from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import api.models as models
import api.serializers as serializers


class FindingViewSet(viewsets.ModelViewSet):
    queryset = models.Finding.objects.all()
    serializer_class = serializers.FindingSerializer
    permission_classes = (IsAuthenticated, )

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action in ('list', 'retrieve'):
            permission_classes = (IsAuthenticated, )
        return [permission() for permission in permission_classes]

    def list(self, request, pk=None):
        security_test = request.query_params.get('security_test')
        queryset = self.get_queryset()

        if security_test:
            try:
                _ = uuid.UUID(security_test)
            except ValueError:
                print('Bad value for review ID')
                return Response(status=status.HTTP_400_BAD_REQUEST)
            queryset = models.Finding.objects.filter(
                security_test=security_test).order_by('creation_date')

        serializer = self.get_serializer(queryset, many=True)
        response_data = serializer.data

        return Response(response_data)
