import grpc
import sys
import os
import django
from decouple import config
from dotenv import load_dotenv

# Load environment variables
load_dotenv('../.env')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_main.settings')
django.setup()

# Get gRPC server configuration from environment
HOST = config('AUTH_SERVICE_HOST', default='localhost')
PORT = int(config('AUTH_SERVICE_PORT', default='50051'))

# Add the parent directory to the path to import proto files
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

try:
    import auth_service_pb2
    import auth_service_pb2_grpc
except ImportError:
    # If proto files don't exist, we'll handle this gracefully
    print("Proto files not found. Please generate them first.")


class AuthServiceClient:
    def __init__(self, host=None, port=None):
        # Get host and port from environment variables or use defaults
        self.host = HOST
        self.port = PORT
        self.channel = None
        self.stub = None
        print(f"gRPC Client configured for {self.host}:{self.port}")
    
    def connect(self):
        """Establish connection to gRPC server"""
        try:
            self.channel = grpc.insecure_channel(f'{self.host}:{self.port}')
            self.stub = auth_service_pb2_grpc.AuthServiceStub(self.channel)
            
            # Test the connection with a timeout
            grpc.channel_ready_future(self.channel).result(timeout=10)
            print(f"Successfully connected to gRPC server at {self.host}:{self.port}")
            return True
        except grpc.FutureTimeoutError:
            print(f"Timeout connecting to gRPC server at {self.host}:{self.port}")
            return False
        except Exception as e:
            print(f"Failed to connect to gRPC server: {e}")
            return False
    
    def register_user(self, username, password, email=""):
        """Register a new user"""
        if not self.stub:
            if not self.connect():
                return {"success": False, "message": "Failed to connect to auth service"}
        
        try:
            request = auth_service_pb2.RegisterRequest(
                username=username,
                password=password,
                email=email
            )
            response = self.stub.Register(request)
            return {
                "success": response.success,
                "message": response.message,
                "token": response.token
            }
        except Exception as e:
            return {"success": False, "message": f"Registration failed: {str(e)}"}
    
    def login_user(self, username, password):
        """Login user"""
        if not self.stub:
            if not self.connect():
                return {"success": False, "message": "Failed to connect to auth service"}
        
        try:
            request = auth_service_pb2.LoginRequest(
                username=username,
                password=password
            )
            response = self.stub.Login(request)
            return {
                "success": response.success,
                "message": response.message,
                "token": response.token
            }
        except Exception as e:
            return {"success": False, "message": f"Login failed: {str(e)}"}
    
    def logout_user(self, username):
        """Logout user"""
        if not self.stub:
            if not self.connect():
                return {"success": False, "message": "Failed to connect to auth service"}
        
        try:
            request = auth_service_pb2.LogoutRequest(username=username)
            response = self.stub.Logout(request)
            return {
                "success": response.success,
                "message": response.message
            }
        except Exception as e:
            return {"success": False, "message": f"Logout failed: {str(e)}"}
    
    def close(self):
        """Close the gRPC connection"""
        if self.channel:
            self.channel.close()


# Global client instance
auth_client = AuthServiceClient()
