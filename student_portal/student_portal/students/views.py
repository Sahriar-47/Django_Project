from django.shortcuts import render, redirect
from .models import Problem, Solution
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ProblemForm

# API Views
from rest_framework import viewsets
from .serializers import ProblemSerializer, SolutionSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.forms import UserCreationForm


class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    permission_classes = [IsAuthenticated]


class SolutionViewSet(viewsets.ModelViewSet):
    queryset = Solution.objects.all()
    serializer_class = SolutionSerializer
    permission_classes = [IsAuthenticated]


# Template Views
def home(request):
    if request.user.is_authenticated:
        problems = Problem.objects.all()
        return render(request, 'students/home.html', {'problems': problems})
    return redirect('login')


@login_required
def submit_solution(request, problem_id):
    problem = Problem.objects.get(id=problem_id)
    if request.method == 'POST':
        solution_text = request.POST['solution_text']
        Solution.objects.create(problem=problem, student=request.user, solution_text=solution_text)
        return redirect('home')
    return render(request, 'students/submit_solution.html', {'problem': problem})


@login_required
def review_solutions(request):
    if request.user.is_staff:
        solutions = Solution.objects.filter(is_approved=False)
        return render(request, 'students/review_solutions.html', {'solutions': solutions})
    return redirect('home')


@login_required
def approve_solution(request, solution_id):
    if request.user.is_staff:
        solution = Solution.objects.get(id=solution_id)
        solution.is_approved = True
        solution.save()
        return redirect('review_solutions')
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'students/register.html', {'form': form})



# Ensure only staff or admin users can access the view
def is_staff_user(user):
    return user.is_staff

@login_required
@user_passes_test(is_staff_user)
def create_problem(request):
    if request.method == "POST":
        form = ProblemForm(request.POST)
        if form.is_valid(): 
            problem = form.save(commit=False)
            problem.created_by = request.user
            problem.save()
            return redirect('home')  # Redirect to the home page after creating the problem
    else:
        form = ProblemForm()

    return render(request, 'students/create_problem.html', {'form': form})
