from django.db import models
from user.models import CustomUser


class Tag(models.Model):
    """
    Model to store tags, which can be used to classify questions.
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    """
    Model to represent a question.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, related_name="questions")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="questions")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Answer(models.Model):
    """
    Model to represent an answer to a question.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    text = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="answers")
    likes = models.ManyToManyField(CustomUser, related_name="liked_answers", blank=True)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def like_count(self):
        """
        Returns the total number of likes for this answer.
        """
        return self.likes.count()

    def __str__(self):
        return f"Answer to '{self.question.title}' by {self.author.fullname}"
