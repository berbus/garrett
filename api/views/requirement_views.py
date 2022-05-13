from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

import api.models as models
import api.serializers as serializers


class RequirementViewSet(viewsets.ModelViewSet):
    queryset = models.Requirement.objects.all()
    serializer_class = serializers.RequirementSerializer
    permission_classes = (IsAuthenticated, )

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action in ('list', 'retrieve'):
            permission_classes = (IsAuthenticated, )
        return [permission() for permission in permission_classes]
