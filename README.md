# 📄 PDF to Word Converter

Convert PDF files into editable Word (`.docx`) documents in the browser. A **React** frontend with **Tailwind CSS** uploads the PDF to a **FastAPI** backend, which keeps the layout and font styles with **PyMuPDF** and falls back to **Tesseract OCR** for scanned pages.

## Features

- Upload a PDF and download the `.docx`
- Keeps formatting: font sizes, bold text and layout
- **OCR option** for scanned or image-only PDFs
- Clear status messages and error dialogs

## Project layout

```
frontend/   React app (Create React App + Tailwind); posts to http://localhost:8000/convert
backend/    FastAPI service: requirements, setup notes and Tesseract install guide
```

> **Note:** the backend's Python source is not in this repository yet; `backend/` holds its README, requirements and the Tesseract install guide.

## Run the frontend

```bash
cd frontend
npm install
npm start          # http://localhost:3000
```

## Backend requirements

FastAPI · Uvicorn · PyMuPDF · pdfplumber · pypdf · python-docx · pdf2image · pytesseract · Pillow. Tesseract itself must be installed for OCR: see `backend/INSTALL_TESSERACT.md`.

## Tech

React · Tailwind CSS · Axios · Python · FastAPI · PyMuPDF · Tesseract OCR

---

Built by [Muhammad Suleman](https://github.com/Suleman-Saleh)
