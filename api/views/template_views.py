from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

import api.models as models
import api.serializers as serializers


class TemplateViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = models.Template.objects.all()
    serializer_class = serializers.TemplateSerializer

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action in ('list', 'retrieve'):
            permission_classes = (IsAuthenticated, )
        return [permission() for permission in permission_classes]
