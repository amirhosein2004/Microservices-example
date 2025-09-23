from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse


def register_view(request):
    """User registration view"""
    if request.method == 'POST':
        data = request.POST
        user = User.objects.create_user(username=data['username'], password=data['password'])
        login(request, user)
        return JsonResponse({'message': 'User registered successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)


def login_view(request):
    """User login view"""
    if request.method == 'POST':
        data = request.POST
        user = User.objects.get(username=data['username'], password=data['password'])
        login(request, user)
        return JsonResponse({'message': 'User logged in successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)


def logout_view(request):
    """User logout view"""
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'User logged out successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)
