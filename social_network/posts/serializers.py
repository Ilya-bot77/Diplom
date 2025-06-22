from django.template.defaulttags import comment
from rest_framework import serializers

from posts.models import Post, Comment

# Сериализатор для комментариев к постам

class CommentSerializer(serializers.ModelSerializer):
     class Meta:
        model = Comment
        fields = ['author', 'text', 'created_at', 'post']
        read_only_fields = ['author']

# Сериализатор для постов

class PostSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'user', 'text', 'image', 'created_at', 'comment', 'post_like']
        read_only_fields = ['user', 'post_like']