import PyPDF2
from docx import Document

def get_docx_file_content(file_path: str) -> str:
    doc = Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def get_txt_file_content(file_path: str) -> str:
    with open(file_path, 'r') as file:
        text = file.read()
    return text

def get_pdf_file_content(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        for page_num in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_num)
            text += page.extract_text()
    return text

def recognize_function_by_file_extension(file_path: str, extension: str) -> str:
    if extension == "docx":
        return get_docx_file_content(file_path)
    if extension == "pdf":
        return get_pdf_file_content(file_path)
    if extension == "txt":
        return get_txt_file_content(file_path)