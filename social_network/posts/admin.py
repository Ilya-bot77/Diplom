from django.contrib import admin
from posts.models import Post, Comment, Like

# вход в админ панель (admin / admin)

admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(Like)