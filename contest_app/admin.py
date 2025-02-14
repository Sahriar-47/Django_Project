from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Student, Problem, Solution

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'registration_date')
    search_fields = ('name', 'email')

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty')

@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ('student', 'problem', 'solved_on')
