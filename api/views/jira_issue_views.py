from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import api.models as models
import api.serializers as serializers
import api.services as services


class JiraIssueViewSet(viewsets.ModelViewSet):
    queryset = models.JiraIssue.objects.all()
    serializer_class = serializers.JiraIssueSerializer
    permission_classes = (IsAuthenticated, )

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action in ('list', 'retrieve'):
            permission_classes = (IsAuthenticated, )
        return [permission() for permission in permission_classes]

    def list(self, request):
        services.jira.update_jira_issues_db()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            self.get_queryset().filter(status=services.jira.INITIAL_ISSUE_STATE), many=True)
        return Response(serializer.data)
