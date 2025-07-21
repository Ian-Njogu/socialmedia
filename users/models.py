from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField

# Create your models here.
class User(AbstractUser):
    profile_picture = CloudinaryField('image', null=True, blank=True)
    bio = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.username