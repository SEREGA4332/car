from rest_framework import serializers
from main.models import  Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'text', 'created_at']
        read_only_fields = ['created_at']


class PostSerializer(serializers.ModelSerializer):
  comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'author', 'text', 'image', 'created_at', 'comments', 'likes_count']
        read_only_fields = ['author', 'likes_count']

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Like
        fields = ['id', 'user', 'post']
        read_only_fields = ['user']

    def get_likes_count(self, obj):
        return obj.likes.count()