from django.db import models
from users.models import User
from cloudinary.models import CloudinaryField

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    image = CloudinaryField('image', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hashtags = models.CharField(max_length=255, blank=True)
   
    def __str__(self):
        return f"{self.user.username} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
   
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return f"{self.user.username} on {self.post.id} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True, related_name='likes')
   
class Meta:
    unique_together = ('post', 'user')
   
    def __str__(self):
        return f"{self.user.username}"
   
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)
   
class Meta:
    unique_together = ('follower', 'following')
   
    def __str__(self):
        return f"{self.follower.username} follows {self.following.username} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
