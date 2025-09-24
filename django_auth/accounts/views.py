from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
import uuid


# gRPC functions
def register_user_grpc(username, password, email=""):
    """Register user via gRPC"""
    try:
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            return {
                'success': False,
                'message': 'کاربری با این نام کاربری قبلاً ثبت شده است'
            }
        
        # Create new user
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        
        # Generate a simple token (in production, use proper JWT or session tokens)
        token = str(uuid.uuid4())
        
        return {
            'success': True,
            'message': 'کاربر با موفقیت ثبت شد',
            'token': token
        }
        
    except IntegrityError:
        return {
            'success': False,
            'message': 'خطا در ثبت کاربر - نام کاربری تکراری است'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'خطا در ثبت کاربر: {str(e)}'
        }


def login_user_grpc(username, password):
    """Login user via gRPC"""
    try:
        # Authenticate user
        user = authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_active:
                # Generate a simple token
                token = str(uuid.uuid4())
                
                return {
                    'success': True,
                    'message': 'ورود موفقیت‌آمیز بود',
                    'token': token
                }
            else:
                return {
                    'success': False,
                    'message': 'حساب کاربری غیرفعال است'
                }
        else:
            return {
                'success': False,
                'message': 'نام کاربری یا رمز عبور اشتباه است'
            }
            
    except Exception as e:
        return {
            'success': False,
            'message': f'خطا در ورود: {str(e)}'
        }


def logout_user_grpc(username):
    """Logout user via gRPC"""
    try:
        logout(username)
        # In a real implementation, you would invalidate the user's token here
        # For now, we'll just return a success message
        return {
            'success': True,
            'message': 'خروج موفقیت‌آمیز بود'
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'خطا در خروج: {str(e)}'
        }
