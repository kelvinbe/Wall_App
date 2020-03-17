from rest_framework import serializers
from wall.models import Message
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth import authenticate

class MessageSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    def create(self, validated_data):
        return Message.objects.create(**validated_data)


    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.message)
        instance.posted= validated_data.get('posted', instance.posted)
        instance.author = validated_data.get('author', instance.author)
        instance.save()
        return instance

    class Meta:
            model = Message
            fields = ['id', 'title', 'description', 'posted', 'author']



class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(required=True)

    def create(self, validated_data):
        user = User.objects.create_user(username= validated_data['username'],email= validated_data['email'], password=validated_data['password'])

        return user

    class Meta:
                model = User
                fields = ['id','username','email','password']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")
