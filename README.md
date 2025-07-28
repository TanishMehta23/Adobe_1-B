# Adobe Hackathon Challenge 1B - File Analyzer

## What it does
Intelligently analyzes any file and generates detailed JSON reports with metadata, content analysis, and processing insights.

**Supported files:** Text, JSON, CSV, Images, and any other file format

## Quick Start

### 🖥️ Run Locally
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Add files to input/ folder
# 3. Run analyzer
python main.py

# 4. Check results in output/ folder
```

### 🐳 Run with Docker
```bash
# Build
docker build --platform linux/amd64 -t challenge-1b .

# Run (Windows PowerShell)
docker run --rm -v ${PWD}/input:/app/input:ro -v ${PWD}/output:/app/output --network none challenge-1b

# Run (Windows Command Prompt)
docker run --rm -v %cd%/input:/app/input:ro -v %cd%/output:/app/output --network none challenge-1b

# Run (Linux/Mac)
docker run --rm -v $(pwd)/input:/app/input:ro -v $(pwd)/output:/app/output --network none challenge-1b
```

### 🚀 Easy Docker Run (Windows)
```bash
# Using batch script
run_docker.bat

# Using PowerShell script
.\run_docker.ps1
```

## How it works
1. **Drop files** into `input/` directory
2. **Run** `python main.py`
3. **Get results** as JSON files in `output/` directory

## Output Example
Each file generates a JSON report with:
- **File info**: Size, type, timestamps, hash
- **Content analysis**: Text stats, JSON structure, CSV dimensions
- **Smart processing**: Word frequency, sentiment analysis, validation

## Features
✅ Multi-format support  
✅ Intelligent content analysis  
✅ Error handling  
✅ Performance optimized  
✅ Docker ready  
✅ No internet required  

## Requirements
- Python 3.10+
- Dependencies in `requirements.txt`
- For Docker: AMD64 platform support

