import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
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
        self.root.title("PixelCat-Photo v0.1.2")
        self.root.geometry("1000x800")
        self.root.configure(bg="#000000")

        self.bg_color = "#000000"
        self.fg_color = "#ffffff"
        self.batch_files = []
        self.current_img = None

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
        style.configure("Horizontal.TProgressbar", background="#00ff00", troughcolor="#222222")

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
        self.view_canvas.pack(expand=True, fill="both", padx=20, pady=10)

        btn_frame = ttk.Frame(self.viewer_tab)
        btn_frame.pack(fill="x", side="bottom", pady=20)

        ttk.Button(btn_frame, text="Open Image", command=self.open_image_viewer).pack(side="left", padx=20)
        ttk.Button(btn_frame, text="Rotate 90°", command=self.rotate_current).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Save Image", command=self.save_current_viewer).pack(side="left", padx=5)

    def setup_converter_tab(self):
        ttk.Label(self.converter_tab, text="Drag & Drop Files Below", font=("Arial", 14)).pack(pady=10)

        self.file_listbox = tk.Listbox(self.converter_tab, bg="#111111", fg="white", borderwidth=0, height=12)
        self.file_listbox.pack(fill="x", padx=40, pady=5)

        self.file_listbox.drop_target_register(DND_FILES)
        self.file_listbox.dnd_bind('<<Drop>>', self.handle_drop)

        btn_row = ttk.Frame(self.converter_tab)
        btn_row.pack(pady=10)
        ttk.Button(btn_row, text="Clear List", command=self.clear_batch_list).pack()

        self.format_var = tk.StringVar(value="PNG")
        ttk.OptionMenu(self.converter_tab, self.format_var, "PNG", "PNG", "JPEG", "BMP", "ICO").pack(pady=5)

        self.progress = ttk.Progressbar(self.converter_tab, orient="horizontal", length=400, mode="determinate",
                                        style="Horizontal.TProgressbar")
        self.progress.pack(pady=20)

        ttk.Button(self.converter_tab, text="Start Batch Conversion", command=self.run_batch).pack(pady=10)

    def handle_drop(self, event):
        files = self.root.tk.splitlist(event.data)
        for f in files:
            clean_path = f.replace('{', '').replace('}', '')  # Handle Windows paths with spaces
            if clean_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')) and clean_path not in self.batch_files:
                self.batch_files.append(clean_path)
                self.file_listbox.insert(tk.END, os.path.basename(clean_path))

    def open_image_viewer(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp")])
        if path:
            self.current_img = Image.open(path)
            self.display_image()

    def rotate_current(self):
        if self.current_img:
            self.current_img = ImageLogic.rotate_image(self.current_img)
            self.display_image()

    def save_current_viewer(self):
        if self.current_img:
            save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("BMP", "*.bmp")])
            if save_path:
                if ImageLogic.save_viewer_image(self.current_img, save_path):
                    messagebox.showinfo("Success", "Image saved successfully!")

    def display_image(self):
        temp_img = self.current_img.copy()
        temp_img.thumbnail((900, 600))
        self.photo = ImageTk.PhotoImage(temp_img)
        self.view_canvas.delete("all")
        self.root.update_idletasks()
        self.view_canvas.create_image(self.view_canvas.winfo_width() // 2, self.view_canvas.winfo_height() // 2,
                                      image=self.photo)

    def clear_batch_list(self):
        self.batch_files = []
        self.file_listbox.delete(0, tk.END)
        self.progress['value'] = 0

    def update_progress(self, current, total):
        val = (current / total) * 100
        self.progress['value'] = val
        self.root.update_idletasks()

    def run_batch(self):
        if not self.batch_files: return
        out_dir = filedialog.askdirectory()
        if out_dir:
            success, total = ImageLogic.batch_convert(self.batch_files, out_dir, self.format_var.get(),
                                                      self.update_progress)
            messagebox.showinfo("Batch Complete", f"Processed {success}/{total} files.")


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = PixelCatApp(root)
    root.mainloop()