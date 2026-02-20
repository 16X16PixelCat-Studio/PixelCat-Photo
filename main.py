import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
import sys
from converter import ImageLogic


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class PixelCatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PixelCat-Photo v0.1.0")
        self.root.geometry("1000x700")
        self.root.configure(bg="#1e1e1e")

        self.bg_color = "#1e1e1e"
        self.fg_color = "#ffffff"
        self.accent_color = "#333333"

        # Set App Icon using the resource_path utility
        icon_path = resource_path(os.path.join("assets", "Pixelcat-photo.png"))
        if os.path.exists(icon_path):
            self.icon_img = ImageTk.PhotoImage(file=icon_path)
            self.root.iconphoto(False, self.icon_img)

        self.setup_styles()
        self.setup_ui()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('default')
        style.configure("TNotebook", background=self.bg_color, borderwidth=0)
        style.configure("TNotebook.Tab", background=self.accent_color, foreground=self.fg_color, padding=[10, 5])
        style.map("TNotebook.Tab", background=[("selected", "#444444")])
        style.configure("TFrame", background=self.bg_color)
        style.configure("TLabel", background=self.bg_color, foreground=self.fg_color)
        style.configure("TButton", background=self.accent_color, foreground=self.fg_color)

    def setup_ui(self):
        self.tab_control = ttk.Notebook(self.root)
        self.viewer_tab = ttk.Frame(self.tab_control)
        self.converter_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.viewer_tab, text='Photo Viewer')
        self.tab_control.add(self.converter_tab, text='Converter')
        self.tab_control.pack(expand=1, fill="both")

        self.setup_viewer_tab()
        self.setup_converter_tab()

    def setup_viewer_tab(self):
        self.view_canvas = tk.Canvas(self.viewer_tab, bg="#121212", highlightthickness=0)
        self.view_canvas.pack(expand=True, fill="both", padx=10, pady=10)
        controls = ttk.Frame(self.viewer_tab)
        controls.pack(fill="x", side="bottom", pady=10)
        ttk.Button(controls, text="Open Image", command=self.open_image_viewer).pack()

    def setup_converter_tab(self):
        ttk.Label(self.converter_tab, text="PixelCat Universal Converter", font=("Arial", 16, "bold")).pack(pady=20)
        self.file_label = ttk.Label(self.converter_tab, text="No file selected")
        self.file_label.pack(pady=10)
        ttk.Button(self.converter_tab, text="Select Source File", command=self.select_file_converter).pack(pady=5)

        self.format_var = tk.StringVar(value="PNG")
        self.format_menu = ttk.OptionMenu(self.converter_tab, self.format_var, "PNG", "PNG", "JPEG", "BMP", "ICO")
        self.format_menu.pack(pady=15)
        ttk.Button(self.converter_tab, text="Convert & Export", command=self.run_conversion).pack(pady=30)

    def open_image_viewer(self):
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.pixil *.bmp")])
        if file_path:
            img = ImageLogic.load_pixil_to_pillow(file_path) if file_path.lower().endswith('.pixil') else Image.open(
                file_path)
            if img:
                img.thumbnail((800, 500))
                self.photo = ImageTk.PhotoImage(img)
                self.view_canvas.delete("all")
                # Wait for canvas to update size to center correctly
                self.root.update_idletasks()
                cx = self.view_canvas.winfo_width() // 2
                cy = self.view_canvas.winfo_height() // 2
                self.view_canvas.create_image(cx, cy, image=self.photo, anchor="center")

    def select_file_converter(self):
        self.input_file = filedialog.askopenfilename()
        if self.input_file:
            self.file_label.config(text=f"Selected: {os.path.basename(self.input_file)}")

    def run_conversion(self):
        if hasattr(self, 'input_file') and self.input_file:
            ext = self.format_var.get().lower()
            save_path = filedialog.asksaveasfilename(defaultextension=f".{ext}")
            if save_path and ImageLogic.convert_image(self.input_file, save_path, self.format_var.get()):
                messagebox.showinfo("Success", "Done!")
        else:
            messagebox.showwarning("Warning", "Select file first.")


if __name__ == "__main__":
    root = tk.Tk()
    app = PixelCatApp(root)
    root.mainloop()