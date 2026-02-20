import json
import io
import os
from PIL import Image


class ImageLogic:
    """
    Core logic for PixelCat-Photo v0.1.0
    Handles Pixilart parsing, standard format conversion, and SVG rasterization.
    """

    @staticmethod
    def load_pixil_to_pillow(file_path):
        """
        Parses a .pixil file and converts the first frame/layer into a PIL Image.
        """
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)

            width = data['width']
            height = data['height']

            # Pixilart stores pixel data in a flat list: [r, g, b, a, r, g, b, a...]
            pixel_data = data['frames'][0]['layers'][0]['pixelData']

            # Convert list to bytes for Pillow
            image = Image.frombytes('RGBA', (width, height), bytes(pixel_data))
            return image
        except Exception as e:
            print(f"Error loading .pixil file: {e}")
            return None

    @staticmethod
    def convert_image(input_path, output_path, output_format):
        """
        Generic converter supporting PNG, JPEG, and .pixil exports.
        """
        try:
            if input_path.lower().endswith('.pixil'):
                img = ImageLogic.load_pixil_to_pillow(input_path)
            else:
                img = Image.open(input_path)

            if img is None:
                return False

            # Handle JPEG transparency (convert RGBA to RGB)
            if output_format.upper() in ['JPEG', 'JPG'] and img.mode == 'RGBA':
                img = img.convert('RGB')

            img.save(output_path, format=output_format)
            return True
        except Exception as e:
            print(f"Conversion error: {e}")
            return False