from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def about_me(request):
    return render(request, 'about.html', {})
