from django.http import Http404, HttpResponse
from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet

from posts.permissions import IsOwnerOrReadOnly, UpdateComment
from posts.models import Post, Comment, Like
from posts.serializers import PostSerializer, CommentSerializer

# Класс для работы с постами.

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

# Функция для автоматической подстановки автора поста в поле user при создании поста.

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

# Класс для работы с комментариями.

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, UpdateComment]

    # Функция для автоматической подстановки автора комментария в поле author при создании комментария.

    def perform_create(self, serializer):
        serializer.save(author = self.request.user)

# Установка лайков для постов

@api_view(['GET'])
def like_function (request, post_id, is_like):
    try:
        post = Post.objects.get(id=post_id)
    except:
        raise Http404("Пост не найден!")
    old_like = Like.objects.filter(like_user=request.user, for_post=post)
    if old_like:
        like = Like.objects.get(like_user=request.user, for_post=post)
        if int(like.like_status) == 1 and is_like == 1:
            like.like_status = 0
            like.save()
            post.post_like -= 1
            post.save()
        elif int(like.like_status) == 0 and is_like == 1:
            like.like_status = 1
            like.save()
            post.post_like += 1
            post.save()
    else:
        new_like = Like(like_user=request.user, for_post=post, like_status=is_like)
        new_like.save()
        post.post_like += 1
        post.save()
    return HttpResponse("Статус лайка обновлен")