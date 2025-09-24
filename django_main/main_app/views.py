from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm, LoginForm
import sys
import os

# Add grpc directory to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'grpc'))

try:
    from grpc_client import auth_client
except ImportError:
    # Fallback if grpc_client is not available
    class DummyAuthClient:
        def register_user(self, username, password, email=""):
            return {"success": False, "message": "سرویس احراز هویت در دسترس نیست"}
        def login_user(self, username, password):
            return {"success": False, "message": "سرویس احراز هویت در دسترس نیست"}
        def logout_user(self, username):
            return {"success": True, "message": "خروج انجام شد"}
    
    auth_client = DummyAuthClient()


def home(request):
    """Home page with login and register options"""
    return render(request, 'main_app/home.html')


def register_view(request):
    """User registration view"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data.get('email', '')
            
            # Send request to auth service via gRPC
            result = auth_client.register_user(username, password, email)
            
            if result['success']:
                messages.success(request, result['message'])
                return redirect('login')
            else:
                messages.error(request, result['message'])
    else:
        form = RegisterForm()
    
    return render(request, 'main_app/register.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Send request to auth service via gRPC
            result = auth_client.login_user(username, password)
            
            if result['success']:
                request.session['username'] = username
                request.session['token'] = result.get('token', '')
                messages.success(request, result['message'])
                return redirect('dashboard')
            else:
                messages.error(request, result['message'])
    else:
        form = LoginForm()
    
    return render(request, 'main_app/login.html', {'form': form})


def logout_view(request):
    """User logout view"""
    username = request.session.get('username')
    if username:
        # Send request to auth service via gRPC
        result = auth_client.logout_user(username)
        messages.info(request, result['message'])
        
        # Clear session
        request.session.flush()
    
    return redirect('home')


def dashboard(request):
    """User dashboard"""
    if 'username' not in request.session:
        messages.error(request, 'لطفا ابتدا وارد شوید')
        return redirect('login')
    
    username = request.session['username']
    return render(request, 'main_app/dashboard.html', {'username': username})
