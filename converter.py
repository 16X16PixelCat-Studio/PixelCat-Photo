import os
from PIL import Image


class ImageLogic:
    """
    Core logic for PixelCat-Photo v0.1.2.
    Handles rotation, single saves, and batch processing.
    """

    @staticmethod
    def rotate_image(img):
        """Rotates a PIL Image 90 degrees clockwise."""
        return img.rotate(-90, expand=True)

    @staticmethod
    def save_viewer_image(img, output_path):
        """Saves the image currently in the viewer."""
        try:
            ext = os.path.splitext(output_path)[1].lower()
            # Handle formats that don't support transparency
            if ext in ['.jpg', '.jpeg', '.bmp'] and img.mode == 'RGBA':
                img = img.convert('RGB')

            img.save(output_path)
            return True
        except Exception as e:
            print(f"Save error: {e}")
            return False

    @staticmethod
    def convert_single_image(input_path, output_path, output_format):
        try:
            img = Image.open(input_path)
            if output_format.upper() in ['JPEG', 'JPG', 'BMP'] and img.mode == 'RGBA':
                img = img.convert('RGB')

            if output_format.upper() == 'ICO':
                icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
                img.save(output_path, format='ICO', sizes=icon_sizes)
            else:
                img.save(output_path, format=output_format)
            return True
        except Exception as e:
            print(f"Conversion error: {e}")
            return False

    @staticmethod
    def batch_convert(input_paths, output_folder, output_format, progress_callback=None):
        success_count = 0
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        total = len(input_paths)
        for i, path in enumerate(input_paths):
            file_name = os.path.splitext(os.path.basename(path))[0]
            target_path = os.path.join(output_folder, f"{file_name}.{output_format.lower()}")
            if ImageLogic.convert_single_image(path, target_path, output_format):
                success_count += 1
            if progress_callback:
                progress_callback(i + 1, total)
        return success_count, total