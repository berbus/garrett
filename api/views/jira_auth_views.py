import os

from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import api.services as services

DJ_FE_ENDPOINT = os.getenv('DJ_FE_ENDPOINT')


class JiraAuthViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, )

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action in ('authorize', ):
            permission_classes = tuple()
        return [permission() for permission in permission_classes]

    @action(methods=['GET'], detail=False)
    def status(self, request):
        email = request.user.email
        authenticated = services.jira_auth.user_authenticated(email)
        res = {'authenticated': authenticated, 'url': None}
        if not authenticated:
            res['url'] = services.jira_auth.get_authorization_url(email)
        return Response(res)

    @action(methods=['GET'], detail=False)
    def authorize(self, request):
        auth_code = request.GET['code']
        state = request.GET['state']
        email = services.jira_auth.get_email_from_secret(state)
        services.jira_auth.exchange_code_for_token(email, auth_code, state)
        return redirect(f'{DJ_FE_ENDPOINT}/settings')
