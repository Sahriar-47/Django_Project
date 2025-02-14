from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import SolutionSubmissionForm
from contest_app.models import Solution

def submit_solution(request):
    if request.method == 'POST':
        form = SolutionSubmissionForm(request.POST)
        if form.is_valid():
            solution = form.save(commit=False)
            solution.student = request.user
            solution.save()
            return redirect('student_profile')
    else:
        form = SolutionSubmissionForm()
    return render(request, 'solutions/submit_solution.html', {'form': form})

def student_profile(request):
    solutions = Solution.objects.filter(student=request.user).order_by('-submitted_at')
    return render(request, 'users/student_profile.html', {'solutions': solutions})
