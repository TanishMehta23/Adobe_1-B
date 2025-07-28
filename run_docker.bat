@echo off
echo Adobe Hackathon Challenge 1B - Docker Runner
echo =============================================

REM Check if Docker is available
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not installed or not in PATH
    echo Please install Docker Desktop from: https://www.docker.com/products/docker-desktop/
    pause
    exit /b 1
)

echo Docker found. Building image...
docker build --platform linux/amd64 -t challenge-1b .
if errorlevel 1 (
    echo ERROR: Failed to build Docker image
    pause
    exit /b 1
)

echo Build successful. Running container...
docker run --rm -v %cd%/input:/app/input:ro -v %cd%/output:/app/output --network none challenge-1b
if errorlevel 1 (
    echo ERROR: Failed to run container
    pause
    exit /b 1
)

echo Processing completed successfully!
echo Check the output/ directory for results.
pause
