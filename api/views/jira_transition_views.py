from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import api.models as models
import api.serializers as serializers
import api.services as services


class JiraTransitionViewSet(viewsets.ModelViewSet):
    queryset = models.JiraTransition.objects.all()
    serializer_class = serializers.JiraTransitionSerializer
    permission_classes = (IsAuthenticated, )

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action in ('list', 'retrieve'):
            permission_classes = (IsAuthenticated, )
        return [permission() for permission in permission_classes]

    @action(methods=['GET'], detail=False)
    def garrett_actions(self, request):
        return Response(models.JiraTransition.GarrettActions.values)

    @action(methods=['GET'], detail=False)
    def statuses(self, request):
        return Response(services.jira.get_jira_statuses())
