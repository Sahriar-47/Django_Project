from django.shortcuts import render


# Create your views here.
from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import StudentRegistrationForm
from .forms import ProblemForm
from .models import Solution
from django.core.paginator import Paginator

def home(request):
    return render(request, 'home.html', {'title': 'Contestants Project'})

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = StudentRegistrationForm()
    return render(request, 'register.html', {'form': form})

def submit_problem(request):
    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProblemForm()
    return render(request, 'submit_problem.html', {'form': form})

def list_submissions(request):
    submissions = Solution.objects.all().order_by('-solved_on')
    paginator = Paginator(submissions, 5)  # 5 submissions per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'submissions.html', {'page_obj': page_obj})
