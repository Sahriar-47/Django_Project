from django.contrib import admin

# Register your models here.
from .models import  Problem, Solution

@admin.register(Problem)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'name',)
    search_fields = ('created_by', 'name')

@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ('student', 'problem', 'solved_on')
