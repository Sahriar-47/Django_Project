from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Problem(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    difficulty = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Solution(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    solved_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} solved {self.problem.title}"
from django.db import models

# Create your models here.
