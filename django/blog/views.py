from rest_framework import viewsets
from rest_framework.response import Response
from blog.serializers import UserSerializer, PostSerializer
from blog.models import User, Post
from blog import producer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects
    serializer_class = UserSerializer

    def list(self, request):
        queryset = self.queryset.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        print("creating user")
        producer.publish('create_pr', {'use': 'ghghghhg'})
        return Response({})

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
