import os, json, base64, io
from PIL import Image, ImageEnhance

class ImageLogic:
    @staticmethod
    def open_pixil_file(file_path):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            # Pixilart stores image data in a base64 string within the JSON
            base64_str = data['frames'][0]['layers'][0]['src']
            encoded = base64_str.split(",", 1)[1]
            return Image.open(io.BytesIO(base64.b64decode(encoded)))
        except Exception as e:
            print(f"Pixil Load Error: {e}")
            return None

    @staticmethod
    def apply_filters(img, brightness, contrast):
        if img:
            img = ImageEnhance.Brightness(img).enhance(brightness)
            img = ImageEnhance.Contrast(img).enhance(contrast)
        return img

    @staticmethod
    def rotate_image(img):
        return img.rotate(-90, expand=True)

    @staticmethod
    def save_viewer_image(img, output_path):
        try:
            ext = os.path.splitext(output_path)[1].lower()
            if ext in ['.jpg', '.jpeg', '.bmp'] and img.mode == 'RGBA':
                img = img.convert('RGB')
            img.save(output_path)
            return True
        except: return False

    @staticmethod
    def batch_convert(input_paths, output_folder, output_format, progress_callback):
        if not os.path.exists(output_folder): os.makedirs(output_folder)
        for i, path in enumerate(input_paths):
            try:
                img = ImageLogic.open_pixil_file(path) if path.lower().endswith('.pixil') else Image.open(path)
                if img:
                    name = os.path.splitext(os.path.basename(path))[0]
                    out = os.path.join(output_folder, f"{name}.{output_format.lower()}")
                    if output_format.upper() in ['JPEG', 'JPG', 'BMP'] and img.mode == 'RGBA':
                        img = img.convert('RGB')
                    img.save(out, format=output_format)
            except: pass
            progress_callback(i + 1, len(input_paths))