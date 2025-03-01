import os
import logging
import pytesseract
from PIL import Image, ImageEnhance
from tasks import delete_handled_file
from utils.handler.photo_handler_utils import postprocess_text, safe_preprocess_image, extract_text_from_image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_message_photo(image_path: str, lang: str) -> str:
    """Main function to handle image processing and text extraction."""
    try:
        # Check if file exists
        if not os.path.exists(image_path):
            logger.error(f"Image file not found: {image_path}")
            return "Error: Image file not found."

        # Verify file size
        file_size = os.path.getsize(image_path)
        if file_size == 0:
            logger.error(f"Image file is empty: {image_path}")
            return "Error: Image file is empty."

        logger.info(f"Processing image: {image_path}, size: {file_size} bytes")

        # Try to use PIL first as it's generally more robust for initial loading
        try:
            pil_image = Image.open(image_path)
            pil_image.verify()  # Verify the image is valid
            logger.info(f"Successfully opened image with PIL: {image_path}")

            # Re-open because verify() closes the file
            pil_image = Image.open(image_path)

            # Extract text directly with PIL if possible
            extracted_text = pytesseract.image_to_string(pil_image)

            # If text looks good enough, return it
            if len(extracted_text.strip()) > 10:
                cleaned_text = postprocess_text(extracted_text, lang)
                return cleaned_text

            # If basic extraction wasn't good enough, continue with advanced processing
        except Exception as pil_error:
            logger.warning(f"PIL initial processing failed: {str(pil_error)}")

        # Preprocess the image using the safer approach
        preprocessed_image = safe_preprocess_image(image_path)

        if preprocessed_image is None:
            # Fallback to direct PIL processing if OpenCV fails
            logger.warning("OpenCV preprocessing failed, falling back to PIL")
            pil_image = Image.open(image_path)

            # Apply PIL-based preprocessing
            pil_image = pil_image.convert('L')  # Convert to grayscale
            pil_image = ImageEnhance.Contrast(pil_image).enhance(2.0)  # Enhance contrast

            # Extract text with PIL
            extracted_text = pytesseract.image_to_string(pil_image)
        else:
            # Extract text with enhanced settings using the preprocessed image
            extracted_text = extract_text_from_image(preprocessed_image, lang)

        # Postprocess the extracted text
        cleaned_text = postprocess_text(extracted_text, lang)

        return cleaned_text
    except Exception as e:
        logger.error(f"Error in handle_message_photo: {str(e)}", exc_info=True)
        return f"Error processing image: {str(e)}"
    finally:
        # Schedule file deletion regardless of success/failure
        try:
            delete_handled_file.delay(image_path)
        except Exception as e:
            logger.error(f"Failed to schedule file deletion: {str(e)}")
