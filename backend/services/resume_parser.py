import PyPDF2
from docx import Document
import io

def parse_resume(content: bytes, filename: str) -> str:
    """Extract text from PDF or DOCX files"""
    try:
        if filename.lower().endswith('.pdf'):
            return _parse_pdf(content)
        elif filename.lower().endswith('.docx'):
            return _parse_docx(content)
        else:
            return "Unsupported file format"
    except Exception as e:
        return f"Error parsing file: {str(e)}"

def _parse_pdf(content: bytes) -> str:
    """Extract text from PDF"""
    pdf_file = io.BytesIO(content)
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def _parse_docx(content: bytes) -> str:
    """Extract text from DOCX"""
    doc_file = io.BytesIO(content)
    doc = Document(doc_file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text