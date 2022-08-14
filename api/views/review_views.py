import datetime

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import api.models as models
import api.serializers as serializers
import api.services as services


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = (IsAuthenticated, )

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action in ('list', 'retrieve'):
            permission_classes = (IsAuthenticated, )
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == 'retrieve':
            serializer_class = serializers.ReviewDetailSerializer
        return serializer_class

    def perform_create(self, serializer):
        jira_issue = serializer.validated_data.get('jira_issue')
        serializer.save()

        if jira_issue:
            services.jira.transition_jira_issue(jira_issue,
                                                models.JiraTransition.GarrettActions.CREATE_REVIEW)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True)
    def complete(self, request, pk=None):
        review = self.get_object()

        if not review.completion_date:
            review.completion_date = datetime.datetime.now().date()
            review.save()
            if review.jira_issue:
                services.jira.transition_jira_issue(
                    review.jira_issue, models.JiraTransition.GarrettActions.COMPLETE_REVIEW)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(review)

        return Response(serializer.data)
