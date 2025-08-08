# PDF to Word Converter Backend

A FastAPI-based backend service that converts PDF files to Word documents with **preserved formatting and layout**. The converter maintains the original document structure, font sizes, bold text, and formatting to create fully editable Word documents.

## Features

- **Format Preservation**: Maintains original PDF formatting including font sizes, bold text, and layout
- **Fully Editable**: Creates Word documents that are completely editable
- **Smart Text Recognition**: Uses PyMuPDF for advanced text extraction with formatting information
- **OCR Support**: Falls back to OCR for image-based PDFs using Tesseract
- **Multiple Document Types**: Works with CVs, resumes, reports, articles, and any PDF document
- **CORS Enabled**: Ready for frontend integration
- **File Upload Handling**: Automatic cleanup of temporary files

## Prerequisites

### System Dependencies

1. **Python 3.8+**
2. **Tesseract OCR** - Required for OCR functionality (image-based PDFs)
3. **Poppler** - Required for PDF to image conversion (OCR fallback)

### Installing System Dependencies

#### Windows:
1. Install Tesseract: Download from https://github.com/UB-Mannheim/tesseract/wiki
2. Install Poppler: Download from http://blog.alivate.com.au/poppler-windows/
3. Add both to your system PATH

#### macOS:
```bash
brew install tesseract
brew install poppler
```

#### Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
sudo apt-get install poppler-utils
```

## Installation

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Option 1: Using the startup script
```bash
python start_server.py
```

### Option 2: Using uvicorn directly
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Option 3: Using the main file
```bash
python main.py
```

The server will start on `http://localhost:8000`

## API Endpoints

- `GET /` - Health check endpoint
- `POST /convert` - Convert PDF to Word document
  - Accepts: PDF file upload
  - Returns: Word document (.docx file) with preserved formatting

## API Documentation

Once the server is running, you can access:
- Interactive API docs: `http://localhost:8000/docs`
- Alternative API docs: `http://localhost:8000/redoc`

## Testing

### Test with a sample PDF:
```bash
python test_conversion.py path/to/your/document.pdf
```

### Test via API:
```bash
curl -X POST "http://localhost:8000/convert" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your_document.pdf"
```

## How It Works

1. **Format-Aware Extraction**: Uses PyMuPDF to extract text with formatting information (font size, bold, position)
2. **Smart Style Detection**: Automatically detects headings, subheadings, and body text based on font properties
3. **Style Application**: Applies appropriate Word styles to maintain visual hierarchy
4. **OCR Fallback**: For image-based PDFs, uses Tesseract OCR with basic formatting
5. **Fully Editable Output**: Creates Word documents that preserve formatting while being completely editable

## Supported Document Types

- **CVs and Resumes**: Maintains section headers, bullet points, and formatting
- **Reports and Articles**: Preserves headings, paragraphs, and text hierarchy
- **Forms and Documents**: Keeps layout and text positioning
- **Any PDF**: Works with any PDF document type

## Troubleshooting

### Common Issues:

1. **OCR not working:**
   - Ensure Tesseract is installed and in your PATH
   - Test with: `tesseract --version`

2. **PDF conversion failing:**
   - Ensure Poppler is installed and in your PATH
   - Test with: `pdftoppm -h`

3. **Import errors:**
   - Make sure you're in the virtual environment
   - Reinstall requirements: `pip install -r requirements.txt`

4. **Port already in use:**
   - Change the port in `start_server.py` or use a different port
   - Kill the process using the port: `netstat -ano | findstr :8000`

5. **Formatting not preserved:**
   - The PDF might be image-based - OCR will be used automatically
   - Check if the PDF contains selectable text (not just images)

## Development

The application structure:
- `main.py` - Main FastAPI application with formatting preservation
- `requirements.txt` - Python dependencies including PyMuPDF
- `start_server.py` - Development server startup script
- `test_conversion.py` - Test script for conversion functionality
- `README.md` - This file

## Technical Details

### Format Preservation Features:
- **Font Size Detection**: Automatically detects and preserves font sizes
- **Bold Text Recognition**: Identifies and maintains bold formatting
- **Heading Detection**: Smart detection of headings based on font size and content
- **Style Hierarchy**: Creates proper Word document styles for consistency
- **Layout Preservation**: Maintains text positioning and document structure

### Fallback Strategy:
1. **Primary**: PyMuPDF for format-aware extraction
2. **Secondary**: Basic text extraction with simple formatting
3. **Tertiary**: OCR for image-based PDFs
