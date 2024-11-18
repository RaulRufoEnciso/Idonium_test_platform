from django.db import models
from django.contrib.auth.models import AbstractUser

# Create Models Here

class User(AbstractUser):
    is_headhunter = models.BooleanField(default=False)

class Test(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_tests")
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    is_from_json = models.BooleanField(default=False)

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="questions")
    content = models.TextField()
    question_type = models.CharField(
        max_length=50, choices=[("MCQ", "Multiple Choice"), ("TF", "True/False")]
    )
    options = models.JSONField()
    correct_answer = models.CharField(max_length=200)

class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=200)
    is_correct = models.BooleanField()

class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.FloatField()
    completed_at = models.DateTimeField(auto_now_add=True)

