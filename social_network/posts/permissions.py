from rest_framework import permissions

# Ограничение на изменения поста. Только автор поста может изменить свой пост.

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return obj.user == request.user