from django.db import models
from django.contrib.auth.models import User

class Problem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Solution(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    solution_text = models.TextField()
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Solution by {self.student.username} for {self.problem.title}"