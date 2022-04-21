from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


# This class will be used to store a post's user, text, time, and likes
class Posts(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user", blank=False)
    post = models.TextField()
    time_posted = models.DateTimeField(auto_now_add=True, blank=False)
    likes = models.ManyToManyField(
        User, related_name="liked_posts", blank=True)

    def __str__(self):
        return self.post

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "post": self.post,
            "time_posted": self.time_posted,
            "likes": str(self.likes.count()),
        }


# This class is used to get the profiles follow count
class Profile(models.Model):
    profile = models.ForeignKey(User, related_name="profile",
                                on_delete=models.CASCADE, blank=False)

    # people that the user follows
    follows = models.ManyToManyField(
        User, related_name="follows", blank=True)

    def __str__(self):
        return self.profile.username

    def serialize(self):
        return {
            "follows": str(self.follows.count()),
        }
