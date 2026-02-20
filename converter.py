import os
from PIL import Image


class ImageLogic:
    """
    Core logic for PixelCat-Photo v0.1.1.
    Handles standard format conversion, batch processing, and multi-size ICOs.
    """

    @staticmethod
    def convert_single_image(input_path, output_path, output_format):
        """
        Converts a single image. Handles ICO scaling specifically.
        """
        try:
            img = Image.open(input_path)

            # Handle JPEG/BMP transparency
            if output_format.upper() in ['JPEG', 'JPG', 'BMP'] and img.mode == 'RGBA':
                img = img.convert('RGB')

            if output_format.upper() == 'ICO':
                # Generate a standard multi-resolution Windows icon
                icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
                img.save(output_path, format='ICO', sizes=icon_sizes)
            else:
                img.save(output_path, format=output_format)

            return True
        except Exception as e:
            print(f"Error converting {input_path}: {e}")
            return False

    @staticmethod
    def batch_convert(input_paths, output_folder, output_format):
        """
        Processes multiple images and returns (success_count, total_count).
        """
        success_count = 0
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        for path in input_paths:
            file_name = os.path.splitext(os.path.basename(path))[0]
            target_path = os.path.join(output_folder, f"{file_name}.{output_format.lower()}")

            if ImageLogic.convert_single_image(path, target_path, output_format):
                success_count += 1

        return success_count, len(input_paths)