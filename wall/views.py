from django.shortcuts import render
from rest_framework import viewsets
from django.core.mail import send_mail
from rest_framework.reverse import reverse
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate
from wall.models import Message
from walltime.settings import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
from wall.serializers import MessageSerializer, RegisterSerializer, User,LoginSerializer
from rest_framework import renderers
from rest_framework.decorators import api_view
from wall.permissions import IsOwnerOrReadOnly
from rest_framework import permissions, generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from knox.models import AuthToken
import socket



class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


        message_list = MessageViewSet.as_view({
        'get': 'list',
        'post': 'create'
        })
        message_detail = MessageViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
        })

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'message': reverse('message-list', request=request, format=format)
    })




class Regsitration(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.save()
        send_mail(subject= "Welcome to wall",
        message="We welcome you to the wall application",
        from_email=EMAIL_HOST_USER, recipient_list=[user.email],
        fail_silently=False)
        return Response({
        "user": RegisterSerializer(user, context = self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })


class Login(generics.GenericAPIView):
        serializer_class = LoginSerializer
        def post(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception = True)
            user = serializer.validated_data
            return Response({
            "user": RegisterSerializer(user, context = self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
            })

class GetUser(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = RegisterSerializer

    def get_object(self):
        return self.request.user
