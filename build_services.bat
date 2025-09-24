@echo off
echo ========================================
echo Building Microservices
echo ========================================

echo.
echo Building Auth Service...
cd django_auth
docker-compose up -d --build
if %errorlevel% neq 0 (
    echo Error building auth service!
    pause
    exit /b 1
)

echo.
echo Building Main Service...
cd ..\django_main
docker-compose up -d --build
if %errorlevel% neq 0 (
    echo Error building main service!
    pause
    exit /b 1
)

cd ..
echo.
echo ========================================
echo All services built successfully!
echo ========================================

pause
