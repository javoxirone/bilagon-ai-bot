import platform

import pytesseract
from PIL import Image

from tasks import delete_handled_file


def handle_message_photo(image_path: str, lang) -> str:
    extracted_text = _extract_text_from_image(image_path, lang)
    delete_handled_file.delay(image_path)
    return extracted_text


def _extract_text_from_image(image_path: str, lang: str) -> str:
    langs = "eng+rus+uzb"
    img = Image.open(image_path)
    _set_tesseract_cmd()
    extracted_text = pytesseract.image_to_string(img, lang=langs)
    return extracted_text


def _set_tesseract_cmd():
    if platform.system() == 'Windows':
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    elif platform.system() == 'Linux':
        pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # Default path for Ubuntu
    else:
        raise EnvironmentError("Unsupported operating system. Please set the Tesseract command manually.")
