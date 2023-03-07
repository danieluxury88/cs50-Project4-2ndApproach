from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
     registration_date = models.DateTimeField(auto_now_add=True)

     def __str__(self):
         return f'{self.username}'


class Post(models.Model):
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="post")
    content = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    likers = models.ManyToManyField("User", related_name="liked_posts")

    def __str__(self):
        return f'{self.author} said: {self.content} on {self.timestamp.strftime("%d-%m-%Y %H:%M:%S")} )'

    def serialize(self):
        return {
            "id": self.id,
            "author": self.author.email,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likers": [user.id for user in self.likers.all()],
        }


class Follow(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followers")
    follower = models.ForeignKey("User", on_delete=models.CASCADE, related_name="following")

    def __str__(self):
        return f'{self.user} is being followed by {self.follower}'


class Reaction(models.Model):
    class ReactionType(models.IntegerChoices):
        LIKE = 1
        NONE = 0

    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="writer")
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="reactions")
    value = models.IntegerField(choices=ReactionType.choices, default=ReactionType.NONE)

    class Meta:
        # Add a unique constraint on the user and post fields to ensure that a user can only react once to a post
        unique_together = ('post', 'author')

    def __str__(self):
        return f'{self.author} reacted: {self.value} on {self.post.content} by {self.post.author}'