from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm

def registerPage(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    return render(request, 'register.html', {'form': form})

def loginPage(request):
    return render(request, 'login.html')

