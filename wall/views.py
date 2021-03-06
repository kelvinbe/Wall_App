from rest_framework import viewsets
from django.core.mail import send_mail
from rest_framework.reverse import reverse
from rest_framework.response import Response
from wall.models import Message
from walltime.settings import EMAIL_HOST_USER
from wall.serializers import MessageSerializer, RegisterSerializer, User, LoginSerializer
from rest_framework.decorators import api_view
from wall.permissions import IsOwnerOrReadOnly
from rest_framework import permissions, generics
from knox.models import AuthToken
from wall.serializers import UserSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('-posted')
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
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


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class Regsitration(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_mail(subject="Welcome to wall",
                  message="We welcome you to the wall application",
                  from_email=EMAIL_HOST_USER, recipient_list=[user.email],
                  fail_silently=False)
        return Response({
            "user": RegisterSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class Login(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": RegisterSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

