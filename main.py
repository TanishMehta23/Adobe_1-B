#!/usr/bin/env python3

import os
import json
import sys
from pathlib import Path
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_directories():
    input_dir = Path("input")
    output_dir = Path("output")
    
    input_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)
    
    return input_dir, output_dir

def process_files(input_dir, output_dir):
    input_files = list(input_dir.glob("*.*"))
    
    if not input_files:
        logger.warning(f"No input files found in {input_dir}")
        return
    
    logger.info(f"Found {len(input_files)} input files to process")
    
    for input_file in input_files:
        try:
            logger.info(f"Processing {input_file.name}...")
            
            result = process_single_file(input_file)
            
            if input_file.suffix.lower() == '.json':
                output_file = output_dir / f"{input_file.stem}_processed.json"
            else:
                output_file = output_dir / f"{input_file.stem}.json"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Successfully processed {input_file.name} -> {output_file.name}")
            
        except Exception as e:
            logger.error(f"Error processing {input_file.name}: {str(e)}")
            continue

def process_single_file(file_path):
    from app.utils import analyze_file_content, extract_metadata, process_data
    
    try:
        if file_path.suffix.lower() in ['.txt', '.json', '.csv']:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            with open(file_path, 'rb') as f:
                content = f.read()
        
        metadata = extract_metadata(file_path, content)
        
        analysis_result = analyze_file_content(content, file_path.suffix.lower(), file_path)
        
        processed_data = process_data(content, file_path.suffix.lower())
        
        result = {
            "filename": file_path.name,
            "file_size": file_path.stat().st_size,
            "file_type": file_path.suffix.lower(),
            "status": "success",
            "metadata": metadata,
            "analysis": analysis_result,
            "processed_data": processed_data,
            "timestamp": datetime.now().isoformat(),
        }
        
        return result
        
    except Exception as e:
        logger.error(f"Error processing {file_path.name}: {str(e)}")
        return {
            "filename": file_path.name,
            "status": "error",
            "error_message": str(e),
            "timestamp": datetime.now().isoformat(),
        }

def main():
    logger.info("Starting Adobe Hackathon Challenge 1B processing...")
    
    try:
        input_dir, output_dir = setup_directories()
        
        process_files(input_dir, output_dir)
        
        logger.info("Processing completed successfully!")
        
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
