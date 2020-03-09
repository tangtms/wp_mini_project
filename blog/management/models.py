from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Post(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=50)
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    status = models.BooleanField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class Comment(models.Model):
    id = models.IntegerField(primary_key=True)
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)