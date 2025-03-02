import os
from typing import Optional, Dict, Callable
import PyPDF2
from docx import Document


class DocumentParser:
    """
    A class to parse content from various document formats.
    """

    def __init__(self):
        """
        Initialize the DocumentParser with supported file handlers.
        """
        # Register supported file handlers
        self.handlers: Dict[str, Callable] = {
            'docx': self._parse_docx,
            'pdf': self._parse_pdf,
            'txt': self._parse_txt
        }

    def parse_document(self, file_path: str) -> Optional[str]:
        """
        Parse content from a document file.

        :param file_path: Path to the document file
        :type file_path: str
        :return: The text content of the document or None if parsing failed
        :rtype: Optional[str]
        """
        if not os.path.exists(file_path):
            return None

        try:
            # Extract file extension
            _, extension = os.path.splitext(file_path)
            extension = extension.lower().lstrip('.')

            # Check if file type is supported
            if extension not in self.handlers:
                return None

            # Process file using the appropriate handler
            return self.handlers[extension](file_path)

        except Exception:
            return None

    def _parse_docx(self, file_path: str) -> str:
        """
        Parse content from a .docx file.

        :param file_path: Path to the .docx file
        :type file_path: str
        :return: Text content of the document
        :rtype: str
        :raises: Various exceptions from the docx library
        """
        doc = Document(file_path)
        return "\n".join(paragraph.text for paragraph in doc.paragraphs)

    def _parse_pdf(self, file_path: str) -> str:
        """
        Parse content from a .pdf file.

        :param file_path: Path to the .pdf file
        :type file_path: str
        :return: Text content of the PDF
        :rtype: str
        :raises: PyPDF2.errors.PdfReadError: If there are issues reading the PDF
        """
        text = []

        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text.append(page.extract_text())

        return "\n".join(text)

    def _parse_txt(self, file_path: str) -> str:
        """
        Parse content from a .txt file.

        :param file_path: Path to the .txt file
        :type file_path: str
        :return: Text content of the file
        :rtype: str
        :raises: IOError: If there are issues reading the file
        :raises: UnicodeDecodeError: If the file cannot be decoded with the specified encoding
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            # Try alternative encodings if UTF-8 fails
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.read()
