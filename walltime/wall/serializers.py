from rest_framework import serializers
from wall.models import Message
from django.contrib.auth.models import User




class MessageSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    def create(self, validated_data):
        return Message.objects.create(**validated_data)


    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.message = validated_data.get('message', instance.message)
        instance.posted= validated_data.get('posted', instance.posted)
        instance.author = validated_data.get('author', instance.author)
        instance.save()
        return instance

        class Meta:
            model = Message
            fields = ['title', 'message', 'posted', 'author']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    message = serializers.HyperlinkedRelatedField(many=True, view_name='user-detail', read_only=True)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(username = validated_data['username'],email= validated_data['email'], password=validated_data['password'])
        user.save()
        return user

    class Meta:
                model = User
                fields = ['id', 'username', 'message','password', 'email']
