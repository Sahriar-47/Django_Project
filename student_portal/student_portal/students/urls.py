from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import create_problem, ProblemViewSet, SolutionViewSet, home, submit_solution, review_solutions, approve_solution, register
router = DefaultRouter()
router.register(r'problems', ProblemViewSet)
router.register(r'solutions', SolutionViewSet)

urlpatterns = [
    path('', home, name='home'),
    path('submit_solution/<int:problem_id>/', submit_solution, name='submit_solution'),
    path('review_solutions/', review_solutions, name='review_solutions'),
    path('approve_solution/<int:solution_id>/', approve_solution, name='approve_solution'),
    path('api/', include(router.urls)),
    path('register/', register, name='register'),
    path('create_problem/', create_problem, name='create_problem'),
]