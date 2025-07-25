import json
import os
import hashlib
from datetime import datetime
from pathlib import Path
import logging

# PDF processing imports
try:
    import PyPDF2
    import pdfplumber
    import fitz  # PyMuPDF
    PDF_PROCESSING_AVAILABLE = True
except ImportError as e:
    logger.warning(f"PDF processing libraries not available: {e}")
    PDF_PROCESSING_AVAILABLE = False

logger = logging.getLogger(__name__)

def process_pdf_content(file_path):
    """Extract comprehensive information from PDF files."""
    if not PDF_PROCESSING_AVAILABLE:
        return {"error": "PDF processing libraries not available"}
    
    try:
        pdf_info = {
            "text_content": "",
            "page_count": 0,
            "metadata": {},
            "text_analysis": {},
            "processing_method": "advanced_pdf_extraction"
        }
        
        # Method 1: Using PyMuPDF (fitz) for comprehensive extraction
        try:
            with fitz.open(file_path) as doc:
                pdf_info["page_count"] = len(doc)
                pdf_info["metadata"] = doc.metadata
                
                # Extract text from all pages
                full_text = ""
                for page_num in range(len(doc)):
                    page = doc[page_num]
                    full_text += page.get_text() + "\n"
                
                pdf_info["text_content"] = full_text.strip()
                
        except Exception as e:
            logger.warning(f"PyMuPDF extraction failed: {e}, trying PyPDF2")
            
            # Method 2: Fallback to PyPDF2
            try:
                with open(file_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    pdf_info["page_count"] = len(reader.pages)
                    
                    # Extract metadata
                    if reader.metadata:
                        pdf_info["metadata"] = {
                            "title": reader.metadata.get('/Title', ''),
                            "author": reader.metadata.get('/Author', ''),
                            "subject": reader.metadata.get('/Subject', ''),
                            "creator": reader.metadata.get('/Creator', ''),
                            "producer": reader.metadata.get('/Producer', ''),
                            "creation_date": str(reader.metadata.get('/CreationDate', '')),
                            "modification_date": str(reader.metadata.get('/ModDate', ''))
                        }
                    
                    # Extract text
                    full_text = ""
                    for page in reader.pages:
                        full_text += page.extract_text() + "\n"
                    
                    pdf_info["text_content"] = full_text.strip()
                    
            except Exception as e2:
                logger.error(f"PyPDF2 extraction also failed: {e2}")
                pdf_info["error"] = f"Text extraction failed: {str(e2)}"
        
        # Analyze extracted text
        if pdf_info["text_content"]:
            text = pdf_info["text_content"]
            pdf_info["text_analysis"] = {
                "character_count": len(text),
                "word_count": len(text.split()),
                "line_count": len(text.splitlines()),
                "paragraph_count": len([p for p in text.split('\n\n') if p.strip()]),
                "avg_words_per_page": len(text.split()) / pdf_info["page_count"] if pdf_info["page_count"] > 0 else 0,
                "has_content": len(text.strip()) > 0,
                "content_preview": text[:500] + "..." if len(text) > 500 else text
            }
        else:
            pdf_info["text_analysis"] = {
                "has_content": False,
                "extraction_status": "no_text_extracted_or_image_based_pdf"
            }
        
        return pdf_info
        
    except Exception as e:
        logger.error(f"PDF processing failed: {e}")
        return {"error": f"PDF processing failed: {str(e)}"}

def extract_metadata(file_path, content):
    try:
        stat_info = file_path.stat()
        
        if isinstance(content, str):
            content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
        else:
            content_hash = hashlib.md5(content).hexdigest()
        
        metadata = {
            "file_size": stat_info.st_size,
            "created_time": datetime.fromtimestamp(stat_info.st_ctime).isoformat(),
            "modified_time": datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
            "file_hash": content_hash,
            "extension": file_path.suffix.lower(),
            "encoding": "utf-8" if isinstance(content, str) else "binary"
        }
        
        return metadata
        
    except Exception as e:
        logger.error(f"Error extracting metadata: {str(e)}")
        return {"error": str(e)}

def analyze_file_content(content, file_type, file_path=None):
    try:
        analysis = {
            "content_type": file_type,
            "size_analysis": {}
        }
        
        # Special handling for PDF files
        if file_type == '.pdf' and file_path:
            pdf_analysis = process_pdf_content(file_path)
            analysis.update(pdf_analysis)
            return analysis
        
        elif file_type in ['.txt', '.json', '.csv', '.md']:
            if isinstance(content, str):
                analysis.update({
                    "character_count": len(content),
                    "word_count": len(content.split()),
                    "line_count": len(content.splitlines()),
                    "has_special_chars": any(not c.isalnum() and not c.isspace() for c in content),
                })
                
                if file_type == '.json':
                    try:
                        parsed_json = json.loads(content)
                        analysis["json_structure"] = {
                            "is_valid_json": True,
                            "top_level_type": type(parsed_json).__name__,
                            "key_count": len(parsed_json) if isinstance(parsed_json, dict) else "N/A"
                        }
                    except json.JSONDecodeError:
                        analysis["json_structure"] = {"is_valid_json": False}
                        
                elif file_type == '.csv':
                    lines = content.splitlines()
                    analysis["csv_structure"] = {
                        "estimated_rows": len(lines),
                        "estimated_columns": len(lines[0].split(',')) if lines else 0,
                        "has_header": True  # Assumption
                    }
        
        elif file_type in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
            analysis.update({
                "is_image": True,
                "size_bytes": len(content) if isinstance(content, bytes) else len(content.encode())
            })
            
        else:
            analysis.update({
                "is_binary": True,
                "size_bytes": len(content) if isinstance(content, bytes) else len(content.encode())
            })
        
        return analysis
        
    except Exception as e:
        logger.error(f"Error analyzing content: {str(e)}")
        return {"error": str(e)}

def process_data(content, file_type):
    try:
        processed = {
            "processing_method": f"standard_{file_type.replace('.', '')}_processing",
            "processed_at": datetime.now().isoformat()
        }
        
        if file_type == '.json':
            try:
                parsed_data = json.loads(content)
                processed.update({
                    "parsed_successfully": True,
                    "data_summary": generate_json_summary(parsed_data),
                    "validation_status": "valid"
                })
            except json.JSONDecodeError as e:
                processed.update({
                    "parsed_successfully": False,
                    "error": str(e),
                    "validation_status": "invalid"
                })
                
        elif file_type == '.csv':
            lines = content.splitlines()
            processed.update({
                "row_count": len(lines),
                "sample_data": lines[:3] if len(lines) > 0 else [],
                "processing_status": "basic_analysis_complete"
            })
            
        elif file_type == '.txt':
            processed.update({
                "text_processing": {
                    "word_frequency": calculate_word_frequency(content),
                    "sentiment_indicators": detect_sentiment_indicators(content),
                    "text_statistics": {
                        "avg_word_length": calculate_avg_word_length(content),
                        "unique_words": len(set(content.lower().split()))
                    }
                }
            })
            
        else:
            processed.update({
                "generic_processing": True,
                "content_signature": hashlib.md5(
                    content.encode() if isinstance(content, str) else content
                ).hexdigest()[:8]
            })
        
        return processed
        
    except Exception as e:
        logger.error(f"Error processing data: {str(e)}")
        return {"error": str(e)}

def generate_json_summary(data):
    try:
        if isinstance(data, dict):
            return {
                "type": "object",
                "keys": list(data.keys())[:10],  # First 10 keys
                "total_keys": len(data.keys()),
                "nested_objects": sum(1 for v in data.values() if isinstance(v, dict))
            }
        elif isinstance(data, list):
            return {
                "type": "array",
                "length": len(data),
                "first_item_type": type(data[0]).__name__ if data else "empty",
                "sample_items": data[:3] if len(data) <= 3 else data[:3]
            }
        else:
            return {
                "type": type(data).__name__,
                "value": str(data)[:100] + "..." if len(str(data)) > 100 else str(data)
            }
    except Exception:
        return {"error": "Unable to generate summary"}

def calculate_word_frequency(text):
    try:
        words = text.lower().split()
        word_count = {}
        for word in words:
            clean_word = ''.join(c for c in word if c.isalnum())
            if clean_word and len(clean_word) > 2:
                word_count[clean_word] = word_count.get(clean_word, 0) + 1
        
        return dict(sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:5])
    except Exception:
        return {}

def detect_sentiment_indicators(text):
    try:
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'like']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'dislike', 'horrible', 'worst', 'poor']
        
        text_lower = text.lower()
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        return {
            "positive_indicators": positive_count,
            "negative_indicators": negative_count,
            "sentiment_score": positive_count - negative_count
        }
    except Exception:
        return {"error": "Unable to analyze sentiment"}

def calculate_avg_word_length(text):
    try:
        words = text.split()
        if not words:
            return 0
        total_length = sum(len(word.strip('.,!?;:"()[]{}')) for word in words)
        return round(total_length / len(words), 2)
    except Exception:
        return 0

def helper_function():
    pass
