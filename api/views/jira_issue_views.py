from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import api.models as models
import api.serializers as serializers
import api.services as services


class JiraIssueViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.JiraIssueSerializer
    queryset = models.JiraIssue.objects.all()

    def list(self, request):
        issues = services.jira.get_issues(request.user.email)
        return Response(issues)
