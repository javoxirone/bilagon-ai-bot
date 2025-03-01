import cv2
import numpy as np
import re
import os
import platform
import logging
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
from typing import List, Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



def safe_preprocess_image(image_path: str) -> Optional[np.ndarray]:
    """
    A safer version of preprocess_image that handles errors better.

    Returns:
        A preprocessed image as numpy array or None if processing fails
    """
    try:
        # Try to read with OpenCV
        img = cv2.imread(image_path)

        # Check if image was loaded correctly
        if img is None or img.size == 0:
            logger.warning(f"OpenCV couldn't load image at {image_path}")
            return None

        logger.info(f"Successfully opened image with OpenCV: {image_path}")

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply basic processing - aim for reliability over perfection
        # Apply simple thresholding
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        return binary
    except Exception as e:
        logger.error(f"Error in safe_preprocess_image: {str(e)}", exc_info=True)
        return None


def preprocess_image(image_path: str) -> Optional[np.ndarray]:
    """
    Apply various preprocessing techniques to improve OCR accuracy.

    Returns:
        A preprocessed image as numpy array or None if processing fails
    """
    try:
        # Read the image
        img = cv2.imread(image_path)

        # Check if image was loaded correctly
        if img is None:
            logger.warning(f"Failed to load image at {image_path}")
            return None

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )

        # Denoise the image
        denoised = cv2.fastNlMeansDenoising(thresh, None, 10, 7, 21)

        # Try to detect if the image is already clear enough
        # If the image has good contrast, we might not need heavy preprocessing
        if cv2.mean(gray)[0] > 200 or cv2.mean(gray)[0] < 50:
            # For very light or very dark images, use the original with minimal processing
            gray_enhanced = cv2.equalizeHist(gray)
            # Moderate thresholding for clean images
            _, binary = cv2.threshold(gray_enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            return binary

        # For normal images, use more aggressive processing
        # Dilate and erode to enhance text
        kernel = np.ones((1, 1), np.uint8)
        dilated = cv2.dilate(denoised, kernel, iterations=1)
        eroded = cv2.erode(dilated, kernel, iterations=1)

        return eroded
    except Exception as e:
        logger.error(f"Error in preprocess_image: {str(e)}", exc_info=True)
        return None


def extract_text_from_image(image: np.ndarray, lang: str) -> str:
    """
    Extract text from the preprocessed image using Tesseract with optimized settings.

    Args:
        image: Preprocessed image as numpy array
        lang: User language preference

    Returns:
        Extracted text
    """
    try:
        set_tesseract_cmd()

        # Map user language to Tesseract language codes
        language_map = {
            'en': 'eng',
            'ru': 'rus',
            'uz': 'uzb',
        }

        # Default to multiple languages for better detection
        langs = "+".join(["eng", "rus", "uzb"])

        # If user language is known, prioritize it
        if lang in language_map:
            # Put the user's language first
            user_lang = language_map[lang]
            langs = f"{user_lang}+eng+rus+uzb"

        # Convert numpy array back to PIL Image
        pil_image = Image.fromarray(image)

        # Set Tesseract configuration for better accuracy
        config = '--oem 1 --psm 3 -c preserve_interword_spaces=1'

        # Extract text with optimized settings
        extracted_text = pytesseract.image_to_string(
            pil_image,
            lang=langs,
            config=config
        )

        return extracted_text
    except Exception as e:
        logger.error(f"Error in extract_text_from_image: {str(e)}", exc_info=True)
        return f"Error extracting text: {str(e)}"


def postprocess_text(text: str, lang: str) -> str:
    """
    Clean and improve the extracted text.

    Args:
        text: Raw text from OCR
        lang: User language preference

    Returns:
        Cleaned and corrected text
    """
    try:
        if not text or text.isspace():
            return "No text detected in the image."

        # Remove excessive whitespace
        cleaned = re.sub(r'\s+', ' ', text).strip()

        # Remove common OCR errors
        cleaned = cleaned.replace('|', 'I')  # Common OCR mistake
        cleaned = cleaned.replace('0', 'O', 1) if cleaned.startswith(
            '0') else cleaned  # Fix starting with zero instead of O

        # Fix common punctuation issues
        cleaned = re.sub(r'(\w)\.(\w)', r'\1. \2', cleaned)  # Add space after period between words
        cleaned = re.sub(r'([,:;])(\w)', r'\1 \2', cleaned)  # Add space after comma, colon, semicolon

        # Try to detect broken paragraphs and fix them
        cleaned = re.sub(r'(\w)-\s*\n\s*(\w)', r'\1\2', cleaned)  # Fix hyphenated words across lines
        cleaned = re.sub(r'(?<!\n)\n(?!\n)', ' ', cleaned)  # Replace single newlines with spaces
        cleaned = re.sub(r'\n{2,}', '\n\n', cleaned)  # Normalize multiple newlines to just two

        # Remove non-printable characters
        cleaned = ''.join(char for char in cleaned if char.isprintable() or char in ['\n', '\t'])

        # Special handling for internet and code-related content
        cleaned = re.sub(r'wwwv\.', 'www.', cleaned)  # Fix common URL typo
        cleaned = re.sub(r'([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})', r'\1@\2.\3',
                         cleaned)  # Fix email addresses

        return cleaned
    except Exception as e:
        logger.error(f"Error in postprocess_text: {str(e)}", exc_info=True)
        return text  # Return original text if processing fails


def set_tesseract_cmd():
    """Set the Tesseract command path based on the platform."""
    try:
        if platform.system() == 'Windows':
            tesseract_paths = [
                r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
                # Add other common Windows paths here
            ]

            for path in tesseract_paths:
                if os.path.exists(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    logger.info(f"Using Tesseract at: {path}")
                    return

            logger.warning("Tesseract not found in common Windows locations")

        elif platform.system() == 'Linux':
            # Try different common Linux paths
            linux_paths = [
                '/usr/bin/tesseract',
                '/usr/local/bin/tesseract',
                '/opt/tesseract/bin/tesseract'
            ]

            for path in linux_paths:
                if os.path.exists(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    logger.info(f"Using Tesseract at: {path}")
                    return

            logger.warning("Tesseract not found in common Linux locations")

        elif platform.system() == 'Darwin':  # macOS
            mac_paths = [
                '/usr/local/bin/tesseract',
                '/opt/homebrew/bin/tesseract',
                '/opt/local/bin/tesseract'
            ]

            for path in mac_paths:
                if os.path.exists(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    logger.info(f"Using Tesseract at: {path}")
                    return

            logger.warning("Tesseract not found in common macOS locations")

        # If we get here, we couldn't find Tesseract
        logger.warning("Could not find Tesseract in common locations. Using system default.")
    except Exception as e:
        logger.error(f"Error in _set_tesseract_cmd: {str(e)}", exc_info=True)


def perform_additional_ocr_attempts(image_path: str, lang: str) -> List[str]:
    """
    Perform multiple OCR attempts with different preprocessing techniques.
    This can be used as a fallback if the main OCR fails.

    Returns:
        List of different text extraction results
    """
    results = []

    try:
        # Check if the file exists
        if not os.path.exists(image_path):
            logger.error(f"Image file not found for additional OCR: {image_path}")
            return ["No text detected. Image file not found."]

        # Try PIL first as it's more robust
        try:
            pil_img = Image.open(image_path)

            # Attempt 1: Direct PIL processing
            results.append(pytesseract.image_to_string(pil_img))

            # Attempt 2: Grayscale PIL
            gray_pil = pil_img.convert('L')
            results.append(pytesseract.image_to_string(gray_pil))

            # Attempt 3: Enhanced contrast
            enhanced_pil = ImageEnhance.Contrast(gray_pil).enhance(2.0)
            results.append(pytesseract.image_to_string(enhanced_pil))

            # Attempt 4: Sharpened
            sharpened_pil = gray_pil.filter(ImageFilter.SHARPEN)
            results.append(pytesseract.image_to_string(sharpened_pil))

            # Try different PSM modes with PIL
            config = '--oem 1 --psm 6'  # Assume single uniform block of text
            results.append(pytesseract.image_to_string(gray_pil, config=config))

            logger.info(f"Successfully performed PIL-based OCR attempts")

        except Exception as pil_error:
            logger.warning(f"PIL fallback attempts failed: {str(pil_error)}")

        # Now try OpenCV if available
        try:
            # Load the original image with OpenCV
            img = cv2.imread(image_path)

            if img is not None and img.size > 0:
                # Attempt with OpenCV: grayscale
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                results.append(pytesseract.image_to_string(gray))

                # Attempt with OpenCV: inverted image
                inverted = cv2.bitwise_not(gray)
                results.append(pytesseract.image_to_string(inverted))

                # Attempt with OpenCV: thresholding
                _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                results.append(pytesseract.image_to_string(binary))

                logger.info(f"Successfully performed OpenCV-based OCR attempts")
            else:
                logger.warning("OpenCV couldn't load the image for additional attempts")
        except Exception as cv_error:
            logger.warning(f"OpenCV fallback attempts failed: {str(cv_error)}")

        return results
    except Exception as e:
        logger.error(f"Error in perform_additional_ocr_attempts: {str(e)}", exc_info=True)
        return ["Error performing additional OCR attempts"]


def choose_best_result(results: List[str]) -> str:
    """
    Choose the best OCR result from multiple attempts.
    Currently, uses simple heuristics - length and character ratio.

    Returns:
        The best text result
    """
    try:
        if not results:
            return "No text detected in the image."

        # Filter out empty or very short results
        valid_results = [text for text in results if text and len(text.strip()) > 5]

        if not valid_results:
            # If all results are too short, take the longest one
            return max(results, key=lambda x: len(x.strip())) if results else "No meaningful text detected."

        # Simple heuristic: longer text with higher ratio of alphanumeric characters is likely better
        def quality_score(text):
            if not text:
                return 0
            alpha_ratio = sum(c.isalnum() or c.isspace() for c in text) / len(text)
            return len(text) * alpha_ratio

        best_result = max(valid_results, key=quality_score)
        return best_result
    except Exception as e:
        logger.error(f"Error in choose_best_result: {str(e)}", exc_info=True)
        # Return the first non-empty result or an error message
        for result in results:
            if result and not result.isspace():
                return result
        return "Error selecting best OCR result."
