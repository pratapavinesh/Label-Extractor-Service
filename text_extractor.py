import pytesseract
from PIL import Image
import cv2
import numpy as np

def extract_text_from_image(image_path):
    try:
        # Load the image using OpenCV
        img = cv2.imread(image_path)
        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Apply thresholding
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        # Convert back to PIL Image format to use with pytesseract
        img_pil = Image.fromarray(thresh)
        # Extract text
        extracted_text = pytesseract.image_to_string(img_pil)
        return extracted_text.strip()
    except Exception as e:
        return f'Error extracting text: {str(e)}'
