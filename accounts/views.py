import json
import logging

import requests
from django.conf import settings
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import permissions
from rest_framework import status
from rest_framework.authtoken import views
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ParseError
from rest_framework.response import Response

from accounts import models as accounts_models
from accounts import serializers as accounts_serializers

logger = logging.getLogger(__name__)


# Create your views here.
def convert_to_dict(msg):
    return {'detail': msg}


# Create your views here.
class LoginView(views.APIView):

    def post(self, request, *args, **kwargs):

        username = request.data.get('username')
        password = request.data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            user_temp = accounts_models.User.objects.filter(username=username).first()
            if user_temp:
                if user_temp.is_active is False:
                    msg = _('Your account has been disabled.')
                    return Response(convert_to_dict(msg), status=403)

            if user:
                if not user.is_active:
                    msg = _('Your account has been disabled.')
                    return Response(convert_to_dict(msg), status=403)
                elif not user.is_staff:
                    msg = _('Unable to log in with provided credentials.')
                    raise ParseError(convert_to_dict(msg))
            else:
                msg = _('Unable to log in with provided credentials.')
                raise ParseError(convert_to_dict(msg))
        else:
            msg = _('Must include "username" and "password".')
            raise ParseError(convert_to_dict(msg))

        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key,
                         'user': {
                             "first_name": user.first_name,
                             "last_name": user.last_name,
                             "email": user.email,
                             "username": user.username,

                         }
                         }, status=status.HTTP_200_OK)


class ProfileView(views.APIView):
    serializer_class = accounts_serializers.ProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)


    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
