from django.db import models


class Problem(models.Model):
    statement = models.CharField(max_length=2550)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    difficulty = models.CharField(
        max_length=10,
        blank=True,
        choices=[("Hard", "Hard"), ("Easy", "Easy"), ("Medium", "Medium")],
    )


class Solution(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    verdict = models.CharField(max_length=50)
    submitted_at = models.DateTimeField(auto_now_add=True)


class TestCase(models.Model):
    input = models.CharField(max_length=255)
    output = models.CharField(max_length=255)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
