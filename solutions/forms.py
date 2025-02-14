from django import forms
from contest_app.models import Solution

class SolutionSubmissionForm(forms.ModelForm):
    class Meta:
        model = Solution
        fields = ['problem_id', 'solution_text']
        widgets = {
            'solution_text': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
        }
