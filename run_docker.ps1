# Adobe Hackathon Challenge 1B - Docker Runner (PowerShell)
Write-Host "Adobe Hackathon Challenge 1B - Docker Runner" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green

# Check if Docker is available
try {
    $dockerVersion = docker --version 2>$null
    Write-Host "Docker found: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Docker is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Build the Docker image
Write-Host "`nBuilding Docker image..." -ForegroundColor Yellow
try {
    docker build --platform linux/amd64 -t challenge-1b .
    if ($LASTEXITCODE -ne 0) {
        throw "Build failed"
    }
    Write-Host "Build successful!" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Failed to build Docker image" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Run the container
Write-Host "`nRunning container..." -ForegroundColor Yellow
try {
    docker run --rm -v ${PWD}/input:/app/input:ro -v ${PWD}/output:/app/output --network none challenge-1b
    if ($LASTEXITCODE -ne 0) {
        throw "Container run failed"
    }
    Write-Host "`nProcessing completed successfully!" -ForegroundColor Green
    Write-Host "Check the output/ directory for results." -ForegroundColor Cyan
} catch {
    Write-Host "ERROR: Failed to run container" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Read-Host "`nPress Enter to exit"
