from rest_framework import serializers
from posts.models import Post, Comment, Like

# Сериализатор для комментариев к постам

class CommentSerializer(serializers.ModelSerializer):
     class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'created_at', 'post']

# Сериализатор для постов с комментариями и количеством лайков

class PostSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()

    def get_likes_count(self, obj):
        return Like.objects.filter(like_status='like', for_post = obj.id).count()

    class Meta:
        model = Post
        fields = ['id', 'user', 'text', 'image', 'created_at', 'comment', 'likes_count']
        read_only_fields = ['user']




