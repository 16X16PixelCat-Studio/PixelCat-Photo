import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk
import os, sys
from converter import ImageLogic

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class PixelCatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PixelCat-Photo v0.2.0")
        self.root.geometry("1100x800")

        self.batch_files = []
        self.current_img = None
        self.original_img = None
        self.zoom_level = 1.0

        # Icon Loading
        icon_path = resource_path(os.path.join("assets", "Pixelcat-photo.png"))
        if os.path.exists(icon_path):
            self.img_icon = tk.PhotoImage(file=icon_path)
            self.root.wm_iconphoto(True, self.img_icon)

        self.setup_ui()

    def setup_ui(self):
        self.tabview = ctk.CTkTabview(self.root)
        self.tabview.pack(expand=True, fill="both", padx=10, pady=10)
        self.tabview.add("Viewer")
        self.tabview.add("Batch")

        # --- VIEWER ---
        viewer_frame = self.tabview.tab("Viewer")
        self.view_canvas = ctk.CTkCanvas(viewer_frame, bg="#111111", highlightthickness=0)
        self.view_canvas.pack(side="left", expand=True, fill="both", padx=10, pady=10)
        self.view_canvas.bind("<MouseWheel>", self.handle_zoom)

        sidebar = ctk.CTkFrame(viewer_frame, width=200)
        sidebar.pack(side="right", fill="y", padx=10, pady=10)

        ctk.CTkLabel(sidebar, text="Filters", font=("Arial", 16, "bold")).pack(pady=10)

        ctk.CTkLabel(sidebar, text="Brightness").pack()
        self.bright_slider = ctk.CTkSlider(sidebar, from_=0.5, to=2.0, command=self.apply_ui_filters)
        self.bright_slider.set(1.0)
        self.bright_slider.pack(pady=5)

        ctk.CTkLabel(sidebar, text="Contrast").pack()
        self.contrast_slider = ctk.CTkSlider(sidebar, from_=0.5, to=2.0, command=self.apply_ui_filters)
        self.contrast_slider.set(1.0)
        self.contrast_slider.pack(pady=5)

        ctk.CTkButton(sidebar, text="Rotate 90°", fg_color="#333", command=self.rotate_current).pack(pady=10)
        ctk.CTkButton(sidebar, text="Open Image", command=self.open_image_viewer).pack(pady=10)
        ctk.CTkButton(sidebar, text="Save As", fg_color="#2ecc71", command=self.save_current).pack(pady=10)

        # --- BATCH ---
        batch_frame = self.tabview.tab("Batch")
        self.listbox = ctk.CTkTextbox(batch_frame, height=300)
        self.listbox.pack(fill="x", padx=40, pady=20)
        self.listbox.insert("0.0", "Drag and Drop Files Here...")
        self.listbox.drop_target_register(DND_FILES)
        self.listbox.dnd_bind('<<Drop>>', self.handle_drop)

        self.format_menu = ctk.CTkOptionMenu(batch_frame, values=["PNG", "JPEG", "BMP", "ICO"])
        self.format_menu.pack(pady=10)

        self.progress = ctk.CTkProgressBar(batch_frame, width=400)
        self.progress.set(0)
        self.progress.pack(pady=20)

        ctk.CTkButton(batch_frame, text="Start Batch", command=self.run_batch).pack(pady=10)
        ctk.CTkButton(batch_frame, text="Clear List", fg_color="#c0392b", command=self.clear_list).pack()

    def handle_zoom(self, event):
        if self.current_img:
            self.zoom_level *= 1.1 if event.delta > 0 else 0.9
            self.zoom_level = max(0.1, min(self.zoom_level, 5.0))
            self.display_image()

    def open_image_viewer(self):
        path = filedialog.askopenfilename()
        if path:
            self.current_img = ImageLogic.open_pixil_file(path) if path.endswith('.pixil') else Image.open(path)
            self.original_img = self.current_img.copy()
            self.zoom_level = 1.0
            self.display_image()

    def apply_ui_filters(self, _=None):
        if self.original_img:
            self.current_img = ImageLogic.apply_filters(self.original_img, self.bright_slider.get(),
                                                        self.contrast_slider.get())
            self.display_image()

    def rotate_current(self):
        if self.current_img:
            self.current_img = ImageLogic.rotate_image(self.current_img)
            self.original_img = self.current_img.copy()
            self.display_image()

    def display_image(self):
        if not self.current_img: return
        w, h = self.current_img.size
        temp = self.current_img.resize((int(w * self.zoom_level), int(h * self.zoom_level)), Image.Resampling.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(temp)
        self.view_canvas.delete("all")
        self.view_canvas.create_image(self.view_canvas.winfo_width() // 2, self.view_canvas.winfo_height() // 2,
                                      image=self.tk_img)

    def handle_drop(self, event):
        files = self.root.tk.splitlist(event.data)
        if "Drag and Drop" in self.listbox.get("0.0", "end"): self.listbox.delete("0.0", "end")
        for f in files:
            path = f.strip('{}')
            if path not in self.batch_files:
                self.batch_files.append(path)
                self.listbox.insert("end", f"{os.path.basename(path)}\n")

    def clear_list(self):
        self.batch_files = []
        self.listbox.delete("0.0", "end")
        self.progress.set(0)

    def save_current(self):
        if self.current_img:
            path = filedialog.asksaveasfilename(defaultextension=".png")
            if path: ImageLogic.save_viewer_image(self.current_img, path)

    def run_batch(self):
        if not self.batch_files: return
        out = filedialog.askdirectory()
        if out:
            ImageLogic.batch_convert(self.batch_files, out, self.format_menu.get(),
                                     lambda c, t: self.progress.set(c / t) or self.root.update_idletasks())
            messagebox.showinfo("Success", "Batch Complete!")


if __name__ == "__main__":
    class App(ctk.CTk, TkinterDnD.DnDWrapper):
        def __init__(self):
            super().__init__()
            self.TkdndVersion = TkinterDnD._require(self)


    root = App()
    app = PixelCatApp(root)
    root.mainloop()