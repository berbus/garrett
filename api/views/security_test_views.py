import datetime

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import StaticHTMLRenderer

import api.models as models
import api.serializers as serializers
import api.services as services


class SecurityTestViewSet(viewsets.ModelViewSet):
    queryset = models.SecurityTest.objects.all()
    serializer_class = serializers.SecurityTestSerializer
    permission_classes = (IsAuthenticated, )

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action in ('list', 'retrieve'):
            permission_classes = (IsAuthenticated, )
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == 'retrieve':
            serializer_class = serializers.SecurityTestDetailSerializer
        return serializer_class

    def perform_create(self, serializer):
        template = serializer.validated_data.get('template')
        security_test = serializer.save()

        if security_test.review and security_test.review.jira_issue:
            services.jira.transition_issue(self.request.user.email,
                                           security_test.review.jira_issue,
                                           models.JiraTransition.GarrettActions.CREATE_TEST)

        for req in template.requirements.all():
            tc = models.TestCase(security_test=security_test, requirement=req)
            tc.save()

        return Response(serializer.data)

    @action(methods=['GET'], detail=True)
    def complete(self, request, pk=None):
        security_test = self.get_object()

        if not security_test.completion_date:
            security_test.completion_date = datetime.datetime.now().date()
            security_test.save()

            if security_test.review and security_test.review.jira_issue:
                services.jira.transition_issue(self.request.user.email,
                                               security_test.review.jira_issue,
                                               models.JiraTransition.GarrettActions.COMPLETE_TEST)

            services.confluence.write_results(request.user.email, security_test)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(security_test)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True, renderer_classes=[StaticHTMLRenderer])
    def html_report(self, request, pk=None):
        security_test = self.get_object()
        html = services.confluence.get_html_report(security_test)
        return Response(html)
