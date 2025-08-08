# Installing Tesseract OCR for PDF to Word Conversion

Tesseract OCR is required to convert image-based PDFs (scanned documents) to editable Word documents.

## Windows Installation

### Option 1: Using the Official Installer (Recommended)

1. **Download Tesseract:**
   - Go to: https://github.com/UB-Mannheim/tesseract/wiki
   - Download the latest version for Windows (64-bit recommended)
   - Example: `tesseract-ocr-w64-setup-5.3.1.20230401.exe`

2. **Install Tesseract:**
   - Run the installer as Administrator
   - **IMPORTANT:** Check "Add to PATH" during installation
   - Choose installation directory (default is fine)
   - Install additional language data if needed

3. **Verify Installation:**
   - Open Command Prompt or PowerShell
   - Run: `tesseract --version`
   - You should see version information

### Option 2: Using Chocolatey

```bash
choco install tesseract
```

### Option 3: Using Winget

```bash
winget install UB-Mannheim.TesseractOCR
```

## macOS Installation

### Using Homebrew (Recommended)

```bash
brew install tesseract
```

### Verify Installation

```bash
tesseract --version
```

## Linux Installation

### Ubuntu/Debian

```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
sudo apt-get install tesseract-ocr-eng  # English language pack
```

### CentOS/RHEL/Fedora

```bash
sudo yum install tesseract
# or
sudo dnf install tesseract
```

## Verifying the Installation

After installation, restart your terminal/command prompt and run:

```bash
tesseract --version
```

You should see output like:
```
tesseract 5.3.1
 leptonica-1.82.0
  libgif 5.2.1 : libjpeg 8d (libjpeg-turbo 2.1.5.1) : libpng 1.6.37 : libtiff 4.4.0 : zlib 1.2.11 : libwebp 1.2.4 : libopenjp2 2.4.0
```

## Troubleshooting

### Windows: "tesseract is not recognized"

1. **Check if Tesseract is in PATH:**
   - Open Command Prompt
   - Run: `echo %PATH%`
   - Look for Tesseract installation directory

2. **Add to PATH manually:**
   - Open System Properties → Advanced → Environment Variables
   - Edit PATH variable
   - Add: `C:\Program Files\Tesseract-OCR` (or your installation path)
   - Restart Command Prompt

3. **Restart your computer** after adding to PATH

### macOS: "command not found"

1. **Check if Homebrew is installed:**
   ```bash
   brew --version
   ```

2. **If not installed, install Homebrew first:**
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

3. **Then install Tesseract:**
   ```bash
   brew install tesseract
   ```

### Linux: "command not found"

1. **Update package lists:**
   ```bash
   sudo apt-get update
   ```

2. **Install Tesseract:**
   ```bash
   sudo apt-get install tesseract-ocr
   ```

## Testing OCR

Create a simple test to verify OCR is working:

1. **Create a test image** with some text
2. **Run OCR:**
   ```bash
   tesseract test_image.png output.txt
   ```
3. **Check the output file** `output.txt` for extracted text

## Additional Language Support

To install additional languages:

### Windows
- Download language data from: https://github.com/tesseract-ocr/tessdata
- Place `.traineddata` files in: `C:\Program Files\Tesseract-OCR\tessdata`

### macOS
```bash
brew install tesseract-lang
```

### Linux
```bash
sudo apt-get install tesseract-ocr-[lang]
# Example: sudo apt-get install tesseract-ocr-fra  # French
```

## After Installation

Once Tesseract is installed and working:

1. **Restart your Python environment**
2. **Test the PDF converter** with an image-based PDF
3. **Check the console output** for OCR processing messages

The PDF to Word converter will now be able to handle:
- ✅ Text-based PDFs (direct extraction)
- ✅ Image-based PDFs (OCR extraction)
- ✅ Scanned documents
- ✅ Complex layouts
- ✅ Any PDF format

