from blog.models import Post, User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):

        is_developer = validated_data.get('is_developer')
        if is_developer:
            print('is_developer is up ')
        shift = User.objects.create(**validated_data)
        return shift

    def update(self, instance, validated_data):
        instance.save()
        return instance


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
