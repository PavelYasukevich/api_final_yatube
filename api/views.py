from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import serializers, viewsets
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)

from .models import Comment, Follow, Group, Post
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer,
)

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = Post.objects.all()
        lookup = self.request.query_params.get("group", None)
        if lookup is not None:
            group = get_object_or_404(Group, pk=lookup)
            return group.posts
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs["post_id"]
        post = get_object_or_404(Post, id=post_id)
        return post.comments

    def perform_create(self, serializer):
        post_id = self.kwargs["post_id"]
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)


class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = GroupSerializer
    queryset = Group.objects.all()


class FollowViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = FollowSerializer

    def get_queryset(self):
        queryset = Follow.objects.all()
        lookup = self.request.query_params.get("search", None)
        if lookup is not None:
            user = get_object_or_404(User, username=lookup)
            return queryset.filter(Q(user=user) | Q(following=user))
        return queryset

    def perform_create(self, serializer):
        author = get_object_or_404(
            User, username=serializer.validated_data["following"]
        )
        if Follow.objects.filter(
            user=self.request.user, following=author
        ).exists():
            raise serializers.ValidationError("Follow already exists!")
        serializer.save(user=self.request.user, following=author)
