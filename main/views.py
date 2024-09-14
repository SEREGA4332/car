from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['POST'])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        # Проверяем, не лайкнул ли уже пользователь этот пост
        if Like.objects.filter(user=user, post=post).exists():
            return Response({'status': 'You have already liked this post'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Создаем новый лайк
        Like.objects.create(user=user, post=post)

        # Увеличиваем счетчик лайков
        post.likes_count += 1
        post.save()

        return Response({'status': 'like added'})

    @action(detail=True, methods=['POST'])
    def unlike(self, request, pk=None):
        post = self.get_object()
        user = request.user

        # Проверяем, существует ли лайк
        try:
            like = Like.objects.get(user=user, post=post)
        except Like.DoesNotExist:
            return Response({'status': 'You have not liked this post'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Удаляем лайк
        like.delete()

        # Уменьшаем счетчик лайков
        if post.likes_count > 0:
            post.likes_count -= 1
            post.save()

        return Response({'status': 'like removed'})



    def create(self, request, *args, **kwargs):
        # Проверяем, не существует ли уже лайк от этого пользователя для этого поста
        post_id = request.data.get('post')
        if Like.objects.filter(user=request.user, post_id=post_id).exists():
            return Response({'detail': 'You have already liked this post.'},
                            status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response({'detail': 'You can only remove your own likes.'},
                            status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)