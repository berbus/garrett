import datetime

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import api.models as models
import api.serializers as serializers
import api.services as services


class ThreatModelViewSet(viewsets.ModelViewSet):
    queryset = models.ThreatModel.objects.all()
    serializer_class = serializers.ThreatModelSerializer
    permission_classes = (IsAuthenticated, )

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action in ('list', 'retrieve'):
            permission_classes = (IsAuthenticated, )
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == 'retrieve':
            serializer_class = serializers.ThreatModelDetailSerializer
        return serializer_class

    def perform_create(self, serializer):
        threat_model = serializer.save()

        if threat_model.review and threat_model.review.jira_issue:
            services.jira.transition_jira_issue(
                threat_model.review.jira_issue,
                models.JiraTransition.GarrettActions.CREATE_THREAT_MODEL)

        return Response(serializer.data)

    @action(methods=['GET'], detail=True)
    def complete(self, request, pk=None):
        threat_model = self.get_object()

        if not threat_model.completion_date:
            threat_model.completion_date = datetime.datetime.now().date()
            threat_model.save()
            if threat_model.review and threat_model.review.jira_issue:
                services.jira.transition_jira_issue(
                    threat_model.review.jira_issue,
                    models.JiraTransition.GarrettActions.COMPLETE_THREAT_MODEL)

            services.confluence.write_results(request.user.email, threat_model)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(threat_model)
        return Response(serializer.data)
