from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden,HttpResponse

def is_admin(user):
    return user.role == 'admin'

@user_passes_test(is_admin)
def admin_only_view(request):
    return HttpResponse("Welcome, Admin!")
