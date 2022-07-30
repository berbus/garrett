import time

from django.contrib.auth import login
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User

# from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from google.oauth2 import id_token
from rest_framework.permissions import IsAuthenticated
from google.auth.transport import requests

import api.models as models
import api.serializers as serializers
from api.apps import ApiConfig

CLIENT_ID = '374530185068-80p56653ls8v4sjfumrfdne860ab5kcn.apps.googleusercontent.com'


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    def create_new_user_from_sso(self, idinfo):
        user = None
        data = {
            'username': idinfo.get('email'),
            'email': idinfo.get('email'),
            'first_name': idinfo.get('given_name'),
            'last_name': idinfo.get('family_name')
        }
        serializer = self.get_serializer(data=data, many=False)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            profile = models.Profile(user=user, picture=idinfo.get('picture'))
            profile.save()

        return user

    def get_permissions(self):
        permission_classes = (IsAuthenticated, )
        if self.action in ('me', 'logout'):
            permission_classes = (IsAuthenticated, )
        elif self.action == 'login':
            permission_classes = ()
        return [permission() for permission in permission_classes]

    @action(methods=['GET'], detail=False)
    def logout(self, request):
        logout(request)
        return Response()

    @action(methods=['POST'], detail=False)
    def login(self, request):
        token = request.POST.get('credential')
        res_data = {}
        res = None

        if token:
            try:
                idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
            except ValueError:
                time.sleep(1)    # Server time one second before Google's cause crash otherwise
                idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

            email = idinfo.get('email')
            try:
                user = User.objects.get(email__exact=email)
            except User.DoesNotExist as e:
                print(f'User with email {email} not found')
                user = self.create_new_user_from_sso(idinfo)

            if user:
                res_data = self.get_serializer(user, many=False).data
                login(request, user)
                res = redirect(ApiConfig.FRONTEND_ENDPOINT, res_data)
            else:
                res = Response(res_data)
        else:
            res = Response()

        return res

    @action(methods=['GET'], detail=False)
    def me(self, request, pk=None):
        res_data = {}
        if request.user and request.user.is_authenticated:
            res_data = self.get_serializer(request.user, many=False).data
            res_data['profile'] = serializers.ProfileSerializer(request.user.profile).data
        return Response(res_data)


class UserDetailView(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
