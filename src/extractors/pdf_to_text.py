"""Extract text from PDFs using PyMuPDF with OCR fallback."""

import fitz
import pytesseract
from PIL import Image
import io
from pathlib import Path


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF with OCR for scanned pages."""
    doc = fitz.open(str(Path(pdf_path).resolve()))
    all_text = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text().strip()
        
        # Use OCR if insufficient text
        if len(text) < 100:
            pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            text = pytesseract.image_to_string(img).strip()
        
        all_text.append(text)
    
    doc.close()
    return "\n\n".join(all_text)