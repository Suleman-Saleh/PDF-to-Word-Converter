# 📄 PDF to Word Converter Backend

A **FastAPI-based backend service** that converts PDF files to Word documents with preserved formatting and layout. It intelligently detects document structure, font styles, and layout, ensuring fully editable and high-quality `.docx` output.

---

## 🚀 Features

- ✅ **Format Preservation**  
  Maintains original formatting (font size, bold, layout) using **PyMuPDF**.

- 📝 **Fully Editable Output**  
  Generates Word documents that can be easily edited in Microsoft Word or Google Docs.

- 🧠 **Smart Text Recognition**  
  Extracts text with formatting info using PyMuPDF (fitz).

- 🔍 **OCR Support**  
  Automatically falls back to **Tesseract OCR** for scanned or image-based PDFs.

- 📄 **Multi-Document Compatibility**  
  Works with resumes, reports, articles, CVs, and more.

- 🌐 **CORS Enabled**  
  Built ready for frontend integration.

- 🗂️ **Temporary File Handling**  
  Automatic cleanup of uploaded and converted files.

---

## ⚙️ Prerequisites

### 🖥️ System Requirements
- Python 3.8+
- **Tesseract OCR** (for scanned/image-based PDFs)
- **Poppler** (used for PDF to image conversion in OCR)

---

## 🧰 Installing System Dependencies

### 🔵 Windows
- Install **Tesseract**: [Tesseract for Windows](https://github.com/UB-Mannheim/tesseract/wiki)
- Install **Poppler**: [Poppler for Windows](http://blog.alivate.com.au/poppler-windows/)
- ➕ Add both installations to your **System PATH**

### 🍎 macOS
```bash
brew install tesseract
brew install poppler
```

### 🐧 Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
sudo apt-get install poppler-utils
```

---

## 🛠 Installation Guide

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   - **Windows**:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. Install Python dependencies:
   ```bash
   pip install fastapi python-docx pytesseract PyMuPDF Pillow uvicorn
   ```

---

## ▶️ Running the Application

Start the server using `uvicorn`:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

📍 The API will be available at: `http://localhost:8000`

---

## 📬 API Endpoints

### `POST /convert`

- **Description**: Convert a PDF to a Word document
- **Request**:
  - Form Data:
    - `file`: PDF file (required)
    - `enable_ocr`: boolean (true/false) – optional
- **Response**: `.docx` file with formatting preserved

---

## 🛠 Troubleshooting

| Issue | Solution |
|-------|----------|
| ❌ OCR not working | Ensure Tesseract is installed and in your PATH. Run `tesseract --version` to check. |
| ❌ PDF conversion failing | Ensure Poppler is installed. Run `pdftoppm -h` to verify. |
| ❌ Import errors | Ensure you're inside the virtual environment. Try `pip install -r requirements.txt`. |
| ❌ Port already in use | Change the port number in the `uvicorn` command. |
| ❌ Formatting not preserved | Check if the PDF is image-based (no selectable text). OCR will handle it. |

---

## 🧪 Technical Details

- 🔍 **Format-Aware Extraction**: Uses PyMuPDF to extract text along with its style (font size, bold, position).
- 🎨 **Smart Style Detection**: Applies heading/body styles based on font properties.
- 📸 **OCR Fallback**: Uses `pytesseract` for scanned PDFs by converting them into images.

---

## 📂 Project Structure

```
pdf-to-word/
├── backend/
│   ├── main.py
│   ├── utils/
│   └── ...
├── frontend/
└── README.md
```

---

## 📧 Contact

For questions or contributions, feel free to open an issue or pull request.

---