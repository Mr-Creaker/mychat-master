# chat/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import CustomUserCreationForm
from .consumers import online_users  # Using the global dictionary from consumers.py

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('chat')
    else:
        form = CustomUserCreationForm()
    return render(request, 'chat/register.html', {'form': form})

@login_required
def chat(request):
    return render(request, 'chat/chat.html')

@staff_member_required
def online_users_view(request):
    # Extract unique usernames from the online_users dictionary.
    active_users = set(online_users.values())
    return render(request, 'chat/online_users.html', {'online_users': sorted(active_users)})
