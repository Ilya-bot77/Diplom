from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet
from posts.permissions import IsOwnerOrReadOnly
from posts.models import Post, Comment, Like
from posts.serializers import PostSerializer, CommentSerializer

# Класс для работы с постами.

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

# Функция для автоматической подстановки автора поста в поле user при создании поста.

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

# Класс для работы с комментариями.

class CommentViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

# Создание комментария к посту при запросе POST по адресу: post/<int:post_id>/comment/

    def create(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            data = request.data
            data['post'] = post_id
            data['author'] = self.request.user.id
            ser = CommentSerializer(data=data)
            if ser.is_valid():
                ser.save()
                return Response(ser.data)
            return Response(ser.errors)
        except Post.DoesNotExist:
            return Response({'message': 'Пост не найден'})

# Изменение комментария при запросе PUT по адресу: post/<int:post_id>/comment/<int:comment_id>/

    def update(self, request, post_id, comment_id):
        try:
            comm = Comment.objects.get(id=comment_id, post=post_id)
            data = request.data
            if comm.author_id == self.request.user.id:
                data['post'] = comm.post_id
                data['author'] = comm.author_id
                ser = CommentSerializer(data=data)
                if ser.is_valid():
                    ser.save()
                    comm.delete()
                    return Response(ser.data)
                return Response(ser.errors)
            else:
                return Response({'message': 'Комментарий не Ваш'})
        except Comment.DoesNotExist:
            return Response({'message': 'Комментарий не найден'})

# Удаление комментария при запросе DELETE по адресу: post/<int:post_id>/comment/<int:comment_id>/

    def destroy(self, request, post_id, comment_id):
        try:
            comm = Comment.objects.get(id=comment_id, post=post_id)
            if comm.author_id == self.request.user.id:
                comm.delete()
            else:
                return Response({'message': 'Комментарий не Ваш'})
            return Response({'message': 'Комментарий удален'})
        except Comment.DoesNotExist:
            return Response({'message': 'Комментарий не найден'})

# Класс для работы с лайками

class LikeViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

# Установка лайков для постов
# Если лайка изначально не было установлено, то делается POST запрос на адрес:
# post/<int:post_id>/like/
# Если при POST запросе появляется сообщение, что like установлен ранее, значит необходимо делать PATCH
# запрос по тому же адресу: post/<int:post_id>/like/

    def create(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            old_like = Like.objects.filter(like_user=self.request.user, for_post=post)
            if old_like:
                return Response({'message': "Like установлен ранее"})
            else:
                new_like = Like(like_user=self.request.user, for_post=post, like_status='like')
                new_like.save()
                return Response({'message':"Like установлен"})
        except Post.DoesNotExist:
            return Response({'message': 'Пост не найден'})

# Установка like, если был none и установка none, если был like.
# Like изменяет свой статус при PATCH запросе по адресу: post/<int:post_id>/like/

    def patch(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            try:
                old_like = Like.objects.get(like_user=self.request.user, for_post=post)
                if old_like.like_status == 'like':
                    old_like.like_status = 'none'
                    old_like.save()
                    return Response({'message': "Like снят"})
                elif old_like.like_status == 'none':
                    old_like.like_status = 'like'
                    old_like.save()
                    return Response({'message': "Like установлен"})
            except Like.DoesNotExist:
                return Response({'message': 'Likes не установлен'})
        except Post.DoesNotExist:
            return Response({'message': 'Пост не найден'})