from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
     registration_date = models.DateTimeField(auto_now_add=True)
#
#
class Post(models.Model):
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="author")
    content = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} said: {self.content} on {self.timestamp.strftime("%d-%m-%Y %H:%M:%S")} )'

    def serialize(self):
        return {
            "id": self.id,
            "author": self.author.email,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }


class Follow(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followers")
    follower = models.ForeignKey("User", on_delete=models.CASCADE, related_name="following")

    def __str__(self):
        return f'{self.user} is being followed by {self.follower}'