# from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
# from fastapi.responses import FileResponse
# from fastapi.middleware.cors import CORSMiddleware
# from docx import Document
# from docx.shared import Inches
# import pytesseract
# import tempfile
# import os
# import shutil
# import re
# import fitz # PyMuPDF
# from PIL import Image
# from io import BytesIO

# app = FastAPI()

# # Configure CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# def cleanup(temp_dir):
#     """Deletes the temporary directory and its contents."""
#     if os.path.exists(temp_dir):
#         shutil.rmtree(temp_dir)
#         print(f"--- Temporary directory cleaned up successfully: {temp_dir} ---")

# def process_pdf_with_ocr_and_tables(pdf_path, doc):
#     """
#     Extracts text from a PDF (including image-based content) using OCR
#     and structures it into a Word document with a proper table.
#     """
#     all_text = ""
#     try:
#         pdf_document = fitz.open(pdf_path)
#         for page_num in range(len(pdf_document)):
#             page = pdf_document.load_page(page_num)
            
#             # First, try to get text directly
#             text_from_page = page.get_text("text")
            
#             # If no text is found, assume it's an image and use OCR
#             if not text_from_page.strip():
#                 pix = page.get_pixmap()
#                 img_data = pix.tobytes("png")
#                 image = Image.open(BytesIO(img_data))
#                 text_from_page = pytesseract.image_to_string(image)
            
#             all_text += text_from_page + "\n\n"
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error during PDF or OCR processing: {e}")

#     if not all_text:
#         doc.add_paragraph("Could not extract any text from the PDF.")
#         return

#     lines = [line.strip() for line in all_text.split('\n') if line.strip()]
    
#     pre_table_text = []
#     post_table_text = []
#     total_lines = []
    
#     table_start_index = -1
#     table_end_index = -1

#     # Find the start of the table by looking for header keywords
#     for i, line in enumerate(lines):
#         if re.search(r'item\s+description', line, re.IGNORECASE):
#             table_start_index = i
#             break
    
#     # Find the end of the table by looking for the "total" line
#     if table_start_index != -1:
#         for i in range(table_start_index + 1, len(lines)):
#             if re.search(r'total exclusive tax amount', lines[i], re.IGNORECASE):
#                 table_end_index = i
#                 total_lines = lines[i:]
#                 break
    
#     if table_start_index != -1 and table_end_index != -1:
#         pre_table_text = lines[:table_start_index]
        
#         # Process the table content
#         table_lines = lines[table_start_index + 1:table_end_index]
        
#         table_data = []
#         current_item = []
        
#         # Regex to detect the start of a new item, handling OCR variations like 'one'
#         item_start_pattern = re.compile(r'^(other|one|a)\s+', re.IGNORECASE)
        
#         for line in table_lines:
#             if item_start_pattern.match(line) and current_item:
#                 table_data.append(" ".join(current_item))
#                 current_item = [line]
#             else:
#                 current_item.append(line)
        
#         if current_item:
#             table_data.append(" ".join(current_item))
        
#         # More robust parsing logic to handle fragmented OCR data
#         parsed_rows = []
#         for item_str in table_data:
#             # Initialize a new row with empty strings
#             row = [""] * 10
            
#             # 1. Item Description and Specification
#             item_spec_match = re.search(r'^(?:other|one|a)\s*(.*?)\s*\((.*?)\)', item_str, re.IGNORECASE)
#             if item_spec_match:
#                 row[0] = item_spec_match.group(1).strip() # Item Description
#                 row[1] = item_spec_match.group(2).strip() # Specification

#             # 2. Unit of Measure and Pack Size
#             unit_pack_match = re.search(r'(EACH|RLS|PKR)\s*(\d+)', item_str, re.IGNORECASE)
#             if unit_pack_match:
#                 row[2] = unit_pack_match.group(1).strip() # Unit Of Measure
#                 row[3] = unit_pack_match.group(2).strip() # Pack Size
            
#             # 3. Prices, Quantity, and Tax.
#             # Use regex to find all currency amounts and numbers
#             price_matches = re.findall(r'PKR\.?\s*([\d,\.]+)', item_str, re.IGNORECASE)
#             if len(price_matches) >= 3:
#                 row[4] = price_matches[0].replace(',', '') # Price
#                 row[6] = price_matches[1].replace(',', '') # Amount
#                 row[7] = price_matches[2].replace(',', '') # Tax Amount
            
#             # 4. Quantity - find a number that isn't part of a price or date
#             quantity_match = re.search(r'(?<!\d)(?<!\d\s)(\d+)(?=\s+(?:PKR|EACH))', item_str)
#             if quantity_match:
#                 row[5] = quantity_match.group(1)
#             elif re.search(r'q', item_str, re.IGNORECASE):
#                 row[5] = '1'

#             # 5. Delivery Dates
#             date_matches = re.findall(r'(\w{3}\s+\d{1,2},\s+\d{4})', item_str)
#             if len(date_matches) >= 2:
#                 row[8] = date_matches[0] # Delivery Date
#                 row[9] = date_matches[1] # Quoted Delivery Date
            
#             parsed_rows.append(row)
#     else:
#         # If no table is found, just add all text as paragraphs
#         pre_table_text = lines
#         parsed_rows = []

#     # Add pre-table text to the document
#     for line in pre_table_text:
#         doc.add_paragraph(line)

#     # Process and add the table
#     if parsed_rows:
#         doc.add_paragraph("PURCHASE ORDER")
#         table_headers = ["Item Description", "Specification", "Unit Of Measure", "Pack Size", "Price", "Quantity", "Amount", "Tax Amount", "Delivery Date", "Quoted Delivery Date"]
#         table = doc.add_table(rows=1, cols=len(table_headers))
#         hdr_cells = table.rows[0].cells
#         for i, header in enumerate(table_headers):
#             hdr_cells[i].text = header

#         for row_data in parsed_rows:
#             row_cells = table.add_row().cells
#             for col_idx, cell_value in enumerate(row_data):
#                 row_cells[col_idx].text = cell_value

#     # Process and add the total amounts from the OCR text
#     if total_lines:
#         doc.add_paragraph("") # Add a blank line for spacing
#         for line in total_lines:
#             doc.add_paragraph(line)
            
# @app.post("/convert")
# async def convert_pdf(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
#     print(f"--- Starting conversion for file: {file.filename} ---")
#     temp_dir = tempfile.mkdtemp()
#     pdf_path = os.path.join(temp_dir, file.filename)
#     docx_path = os.path.join(temp_dir, file.filename.replace('.pdf', '.docx'))

#     try:
#         with open(pdf_path, "wb") as temp_pdf_file:
#             shutil.copyfileobj(file.file, temp_pdf_file)
        
#         doc = Document()
#         process_pdf_with_ocr_and_tables(pdf_path, doc)
#         doc.save(docx_path)
        
#         print("--- OCR and table-based conversion successful. ---")
        
#         background_tasks.add_task(cleanup, temp_dir)
#         return FileResponse(
#             path=docx_path,
#             filename=os.path.basename(docx_path),
#             media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
#         )

#     except HTTPException:
#         raise
#     except Exception as e:
#         print(f"--- An unexpected error occurred: {e} ---")
#         background_tasks.add_task(cleanup, temp_dir)
#         raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}. See backend terminal for details.")
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pdf2docx import parse
import tempfile
import os
import shutil

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# A cleanup function to delete the temporary directory
def cleanup(temp_dir):
    """Deletes the temporary directory and its contents."""
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
        print(f"--- Temporary directory cleaned up successfully: {temp_dir} ---")

@app.post("/convert")
async def convert_pdf(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    print(f"--- Starting conversion for file: {file.filename} ---")

    # Create a temporary directory to store files
    temp_dir = tempfile.mkdtemp()
    pdf_path = os.path.join(temp_dir, file.filename)
    docx_path = os.path.join(temp_dir, file.filename.replace('.pdf', '.docx'))

    try:
        # Save the uploaded PDF file to a temporary location
        with open(pdf_path, "wb") as temp_pdf_file:
            shutil.copyfileobj(file.file, temp_pdf_file)
        
        # Use the pdf2docx library to convert the PDF
        print("--- Attempting PDF to DOCX conversion... ---")
        try:
            parse(pdf_path, docx_path)
            print("--- PDF converted to DOCX successfully. ---")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"PDF to DOCX conversion failed: {e}")

        print(f"--- Word document saved successfully at: {docx_path} ---")

        # Schedule cleanup to run after the file has been sent
        background_tasks.add_task(cleanup, temp_dir)

        return FileResponse(
            path=docx_path,
            filename=os.path.basename(docx_path),
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"--- An unexpected error occurred: {e} ---")
        # Ensure cleanup runs even on error
        background_tasks.add_task(cleanup, temp_dir)
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}. See backend terminal for details.")