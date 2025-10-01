from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'teacher_avaliation/home.html')

# Create your views here.
def login(request):
    return render(request, 'teacher_avaliation/login.html')