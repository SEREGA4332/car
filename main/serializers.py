from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    created_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S.%f')

    class Meta:
        model = Comment
        fields = ['author', 'text', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S.%f')

    class Meta:
        model = Post
        fields = ['id', 'author', 'text', 'image', 'created_at', 'comments', 'likes_count']

    def get_likes_count(self, obj):
        return obj.likes.count()