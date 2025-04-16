from django.db import models
from django.contrib.auth.models import AbstractUser,Permission,Group
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Topic(models.Model):
    topic_name = models.CharField(max_length=80)
    topic_description = models.TextField(blank=True,null=True)
    
    def __str__(self):
        return self.topic_name

class Post(models.Model):
    title = models.CharField(max_length=150,default=" ")
    topic = models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    text = models.TextField()
    image = models.ImageField(upload_to='images/post/',blank=True,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="posts")

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField()
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")
    created_at=models.DateTimeField(auto_now_add=True)

class Like_Dislike(models.Model):
    VOTE_TYPE = [('like','Like'),('dislike','Dislike')]
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    vote_type=models.CharField(max_length=15,choices=VOTE_TYPE)

    class Meta:
        unique_together = ('post','user')

class Reply(models.Model):
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,related_name="replies")
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField()



class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to="profile_pictures/",blank=True,null=True)
    saved_posts = models.ManyToManyField(Post,related_name="saved_post",blank=True)
    groups = models.ManyToManyField(Group,related_name='customuser_groups',blank=True)
    user_permissions = models.ManyToManyField(Permission,related_name='customuser_permissions',blank=True)