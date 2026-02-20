import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
import sys
from converter import ImageLogic


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class PixelCatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PixelCat-Photo v0.1.1")
        self.root.geometry("1000x750")
        self.root.configure(bg="#000000")  # Pure black background

        self.bg_color = "#000000"
        self.fg_color = "#ffffff"
        self.accent_color = "#222222"
        self.batch_files = []

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
        style.configure("TNotebook.Tab", background="#111111", foreground=self.fg_color, padding=[15, 5])
        style.map("TNotebook.Tab", background=[("selected", "#333333")])
        style.configure("TFrame", background=self.bg_color)
        style.configure("TLabel", background=self.bg_color, foreground=self.fg_color)
        style.configure("TButton", background="#333333", foreground=self.fg_color, borderwidth=0)
        style.map("TButton", background=[("active", "#444444")])

    def setup_ui(self):
        self.tab_control = ttk.Notebook(self.root)
        self.viewer_tab = ttk.Frame(self.tab_control)
        self.converter_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.viewer_tab, text=' Photo Viewer ')
        self.tab_control.add(self.converter_tab, text=' Batch Converter ')
        self.tab_control.pack(expand=1, fill="both")

        self.setup_viewer_tab()
        self.setup_converter_tab()

    def setup_viewer_tab(self):
        self.view_canvas = tk.Canvas(self.viewer_tab, bg="#050505", highlightthickness=0)
        self.view_canvas.pack(expand=True, fill="both", padx=20, pady=20)

        btn_frame = ttk.Frame(self.viewer_tab)
        btn_frame.pack(fill="x", side="bottom", pady=20)
        ttk.Button(btn_frame, text="Open Image", command=self.open_image_viewer).pack()

    def setup_converter_tab(self):
        ttk.Label(self.converter_tab, text="Batch Converter", font=("Arial", 18, "bold")).pack(pady=20)

        self.file_listbox = tk.Listbox(self.converter_tab, bg="#111111", fg="white", borderwidth=0, height=10)
        self.file_listbox.pack(fill="x", padx=40, pady=10)

        btn_row = ttk.Frame(self.converter_tab)
        btn_row.pack(pady=10)
        ttk.Button(btn_row, text="Add Files", command=self.add_batch_files).pack(side="left", padx=5)
        ttk.Button(btn_row, text="Clear List", command=self.clear_batch_list).pack(side="left", padx=5)

        ttk.Label(self.converter_tab, text="Convert to:").pack(pady=10)
        self.format_var = tk.StringVar(value="PNG")
        self.format_menu = ttk.OptionMenu(self.converter_tab, self.format_var, "PNG", "PNG", "JPEG", "BMP", "ICO")
        self.format_menu.pack()

        ttk.Button(self.converter_tab, text="Run Batch Conversion", command=self.run_batch).pack(pady=30)

    def open_image_viewer(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp")])
        if path:
            img = Image.open(path)
            img.thumbnail((900, 600))
            self.photo = ImageTk.PhotoImage(img)
            self.view_canvas.delete("all")
            self.root.update_idletasks()
            self.view_canvas.create_image(self.view_canvas.winfo_width() // 2, self.view_canvas.winfo_height() // 2,
                                          image=self.photo)

    def add_batch_files(self):
        files = filedialog.askopenfilenames(filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp")])
        for f in files:
            if f not in self.batch_files:
                self.batch_files.append(f)
                self.file_listbox.insert(tk.END, os.path.basename(f))

    def clear_batch_list(self):
        self.batch_files = []
        self.file_listbox.delete(0, tk.END)

    def run_batch(self):
        if not self.batch_files:
            return messagebox.showwarning("Warning", "Add some files first!")

        out_dir = filedialog.askdirectory(title="Select Output Folder")
        if out_dir:
            success, total = ImageLogic.batch_convert(self.batch_files, out_dir, self.format_var.get())
            messagebox.showinfo("Done", f"Converted {success} of {total} files successfully.")


if __name__ == "__main__":
    root = tk.Tk()
    app = PixelCatApp(root)
    root.mainloop()