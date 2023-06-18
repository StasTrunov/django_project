from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=1000)
    profile_image = models.ImageField(upload_to='static/media/profile_images/', default='static/media/blank-profile-picture.png')
    id_user = models.IntegerField()


class Pweet(models.Model):
    content = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    no_of_likes = models.IntegerField(default=0)


class Comment(models.Model):
    body = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pweet = models.ForeignKey(Pweet, on_delete=models.CASCADE)


class LikedPweet(models.Model):
    post_owner = models.ForeignKey(User,related_name="pweet_owner" ,on_delete=models.CASCADE)
    post = models.ForeignKey(Pweet,related_name="liked_pweet",on_delete=models.CASCADE)
    liker = models.ForeignKey(User,related_name="liked",on_delete=models.CASCADE)

