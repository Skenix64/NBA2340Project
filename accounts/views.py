from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.contrib.auth import views as auth_views

from .forms import CustomUserCreationForm, CustomErrorList, CustomPasswordResetForm

# --------------------
# Logout View
# --------------------
@login_required
def custom_logout_view(request):
    auth_logout(request)
    return redirect('homepage')


# --------------------
# Login View
# --------------------
def login(request):
    template_data = {'title': 'Login'}
    if request.method == 'GET':
        return render(request, 'accounts/login.html', {'template_data': template_data})

    user = authenticate(
        request,
        username=request.POST['username'],
        password=request.POST['password']
    )
    if user is None:
        template_data['error'] = 'The username or password is incorrect.'
        return render(request, 'accounts/login.html', {'template_data': template_data})
    else:
        auth_login(request, user)
        return redirect('homepage')


# --------------------
# Signup View
# --------------------
def signup(request):
    template_data = {'title': 'Sign Up'}
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html', {'template_data': template_data})

    form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
    if form.is_valid():
        form.save()
        return redirect('login')
    else:
        template_data['form'] = form
        return render(request, 'accounts/signup.html', {'template_data': template_data})


# --------------------
# Reset Password Views (Token-based)
# --------------------
reset_tokens = {}

def reset_request_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.filter(username=username).first()

        if user:
            token = get_random_string(32)
            reset_tokens[token] = username
            return redirect('reset_password', token=token)
        else:
            messages.error(request, "Username not found!")

    return render(request, 'accounts/reset_request.html')


def reset_password_view(request, token):
    if token not in reset_tokens:
        messages.error(request, "Invalid or expired token!")
        return redirect('reset_request')

    username = reset_tokens[token]
    user = get_object_or_404(User, username=username)

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if len(new_password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
        elif check_password(new_password, user.password):
            messages.error(request, "New password cannot be the same as the old password.")
        elif new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
        else:
            user.password = make_password(new_password)
            user.save()
            del reset_tokens[token]
            return redirect('login')

    return render(request, 'accounts/reset_password.html', {'token': token})