from rest_framework import generics
from .models import Post
from .serializers import PostSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorOrReadOnly

class PublishPost(generics.CreateAPIView):
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ListPosts(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class RetrieveUpdateDestroyPost(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthorOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)