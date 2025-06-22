from rest_framework import permissions

# Ограничение на изменения поста. Только автор поста может изменить свой пост.

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return obj.user == request.user


# Ограничение на изменения комментария. Только автор комментария может изменить свой комментарий.

class UpdateComment(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return obj.author == request.user
