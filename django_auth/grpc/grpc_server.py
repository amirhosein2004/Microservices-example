import grpc
from concurrent import futures
import sys
import os
import django


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
django.setup()

# Add the parent directory to the path to import proto files
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

try:
    import auth_service_pb2
    import auth_service_pb2_grpc
except ImportError:
    print("Proto files not found. Please generate them first.")
    sys.exit(1)

from accounts.views import register_user_grpc, login_user_grpc, logout_user_grpc


class AuthServiceServicer(auth_service_pb2_grpc.AuthServiceServicer):
    def Register(self, request, context):
        """Handle user registration"""
        try:
            result = register_user_grpc(request.username, request.password, request.email)
            return auth_service_pb2.AuthResponse(
                success=result['success'],
                message=result['message'],
                token=result.get('token', '')
            )
        except Exception as e:
            return auth_service_pb2.AuthResponse(
                success=False,
                message=f"Registration error: {str(e)}",
                token=""
            )
    
    def Login(self, request, context):
        """Handle user login"""
        try:
            result = login_user_grpc(request.username, request.password)
            return auth_service_pb2.AuthResponse(
                success=result['success'],
                message=result['message'],
                token=result.get('token', '')
            )
        except Exception as e:
            return auth_service_pb2.AuthResponse(
                success=False,
                message=f"Login error: {str(e)}",
                token=""
            )
    
    def Logout(self, request, context):
        """Handle user logout"""
        try:
            result = logout_user_grpc(request.username)
            return auth_service_pb2.AuthResponse(
                success=result['success'],
                message=result['message'],
                token=""
            )
        except Exception as e:
            return auth_service_pb2.AuthResponse(
                success=False,
                message=f"Logout error: {str(e)}",
                token=""
            )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_service_pb2_grpc.add_AuthServiceServicer_to_server(AuthServiceServicer(), server)
    
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    
    print(f"Starting gRPC server on {listen_addr}")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
