from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    user = models.ForeignKey(User, verbose_name='Автор поста', on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(upload_to='posts/images',blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    post_like = models.IntegerField(verbose_name='Лайк', default=0)

class Comment(models.Model):
    author = models.ForeignKey(User, verbose_name='Автор комментария', on_delete=models.CASCADE)
    text = models.TextField (max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment')

class Like(models.Model):
    Like_choices = (
        ("like", 1),
        ("none", 0)
    )

    like_user = models.ForeignKey(User, verbose_name='Автор лайка', on_delete=models.CASCADE)
    for_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='like')
    like_status = models.CharField(choices=Like_choices, default=None)
    time_update = models.DateTimeField(auto_now=True)