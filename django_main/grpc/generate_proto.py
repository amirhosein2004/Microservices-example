#!/usr/bin/env python3
"""
Script to generate Python gRPC files from proto definition
"""

import subprocess
import sys
import os

def generate_proto_files():
    """Generate Python files from proto definition"""
    proto_file = "auth_service.proto"
    
    if not os.path.exists(proto_file):
        print(f"Error: {proto_file} not found!")
        return False
    
    try:
        # Generate Python files from proto
        cmd = [
            sys.executable, "-m", "grpc_tools.protoc",
            "--python_out=.",
            "--grpc_python_out=.",
            "--proto_path=.",
            proto_file
        ]
        
        print("Generating Python files from proto...")
        print(f"Running: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Proto files generated successfully!")
            print("Generated files:")
            print("  - auth_service_pb2.py")
            print("  - auth_service_pb2_grpc.py")
            return True
        else:
            print("Error generating proto files:")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except FileNotFoundError:
        print("Error: grpcio-tools not found. Please install it first:")
        print("pip install grpcio-tools")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    success = generate_proto_files()
    sys.exit(0 if success else 1)
