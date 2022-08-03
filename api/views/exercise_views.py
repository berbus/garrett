from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

import api.models as models
import api.serializers as serializers
import api.services as services


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = models.Exercise.objects.all()
    serializer_class = serializers.ExerciseSerializer
    permission_classes = (IsAuthenticated, )

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action in ('list', 'retrieve'):
            permission_classes = (IsAuthenticated, )
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == 'retrieve':
            serializer_class = serializers.ExerciseDetailSerializer
        return serializer_class

    def perform_create(self, serializer):
        template = serializer.validated_data.get('template')
        jira_issue = serializer.validated_data.get('jira_issue')
        exercise = serializer.save()

        if jira_issue:
            services.jira.update_jira_issue(jira_issue,
                                            models.JiraTransition.GarrettActions.CREATE_TEST)

        for req in template.requirements.all():
            tc = models.TestCase(exercise=exercise, requirement=req)
            tc.save()

        response_data = serializer.data
        response_data['service_name'] = exercise.service.name
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()
        if serializer.validated_data.get('finished') and serializer.data.get('jira_issue'):
            jira_id = serializer.data.get('jira_issue')
            jira_issue = models.JiraIssue.objects.get(pk=jira_id)
            services.jira.update_jira_issue(jira_issue,
                                            models.JiraTransition.GarrettActions.COMPLETE_TEST)
        return Response(serializer.data)
