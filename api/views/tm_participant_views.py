import uuid

from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import api.models as models
import api.serializers as serializers


class TMParticipantViewSet(viewsets.ModelViewSet):
    queryset = models.TMParticipant.objects.all()
    serializer_class = serializers.TMParticipantSerializer
    permission_classes = (IsAuthenticated, )

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action in ('list', 'retrieve'):
            permission_classes = (IsAuthenticated, )
        permission_classes = tuple()    # TODO
        return [permission() for permission in permission_classes]

    def list(self, request, pk=None):
        tm_id = request.query_params.get('threat_model')
        queryset = self.get_queryset()
        res = None

        if tm_id:
            try:
                _ = uuid.UUID(tm_id)
            except ValueError:
                print(f'Bad value for Threat Model ID: {tm_id}')
                res = Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                queryset = queryset.filter(threat_model=tm_id)

        if not res:
            serializer = self.get_serializer(queryset, many=True)
            response_data = serializer.data
            res = Response(response_data)

        return res
