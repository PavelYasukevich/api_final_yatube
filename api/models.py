from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts"
    )
    group = models.ForeignKey(
        "Group",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
    )

    def __str__(self):
        fragment = (
            self.text if len(self.text) <= 50 else self.text[:50] + "..."
        )
        date = self.pub_date.strftime("%d %m %Y")
        author = self.author
        return f"{author} - {date} - {fragment}"


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    created = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )


class Group(models.Model):
    title = models.CharField(unique=True, max_length=200)

    def __str__(self):
        return self.title


class Follow(models.Model):
    user = models.ForeignKey(
        User, related_name="follower", on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        User, related_name="following", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ["user", "following"]

    def __str__(self):
        return f"{self.user.username} follows {self.following.username}"
