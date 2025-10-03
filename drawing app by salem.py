# drawing_app.py
import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
import os

# Optional: Pillow improves saving to PNG (needs Ghostscript for PS->PNG on some systems).
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

class DrawingApp:
    def __init__(self, root):
        self.root = root
        root.title("SketchPad — flex on 'em")
        root.geometry("900x600")

        # State
        self.brush_color = "#000000"
        self.bg_color = "#ffffff"
        self.brush_size = 5
        self.last_x = None
        self.last_y = None
        self.drawn_items = []  # stack for undo

        # Layout frames
        control_frame = tk.Frame(root, padx=5, pady=5)
        control_frame.pack(side=tk.LEFT, fill=tk.Y)

        canvas_frame = tk.Frame(root)
        canvas_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        # Canvas
        self.canvas = tk.Canvas(canvas_frame, bg=self.bg_color, cursor="cross")
        self.canvas.pack(expand=True, fill=tk.BOTH)

        # Controls
        tk.Label(control_frame, text="Brush", font=("Arial", 12, "bold")).pack(pady=(0,6))

        tk.Button(control_frame, text="Choose Color", width=15, command=self.choose_color).pack(pady=4)
        tk.Button(control_frame, text="Eraser", width=15, command=self.use_eraser).pack(pady=4)
        tk.Button(control_frame, text="Clear", width=15, command=self.clear).pack(pady=4)
        tk.Button(control_frame, text="Undo (Ctrl+Z)", width=15, command=self.undo).pack(pady=6)

        tk.Label(control_frame, text="Brush size", pady=6).pack()
        self.size_scale = tk.Scale(control_frame, from_=1, to=50, orient=tk.HORIZONTAL, command=self.change_size)
        self.size_scale.set(self.brush_size)
        self.size_scale.pack()

        tk.Button(control_frame, text="Save (Ctrl+S)", width=15, command=self.save).pack(pady=(12,4))

        tk.Label(control_frame, text="Tips", font=("Arial", 10, "italic")).pack(pady=(18,4))
        tk.Label(control_frame, text="• Hold mouse and draw\n• Ctrl+Z undo\n• Ctrl+S save\n• Use Eraser to erase", justify=tk.LEFT).pack()

        # Bindings
        self.canvas.bind("<ButtonPress-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)

        root.bind_all("<Control-z>", lambda e: self.undo())
        root.bind_all("<Control-s>", lambda e: self.save())
        root.bind_all("<Control-S>", lambda e: self.save())

    def choose_color(self):
        color = colorchooser.askcolor(color=self.brush_color, title="Pick brush color")
        if color and color[1]:
            self.brush_color = color[1]

    def use_eraser(self):
        # Eraser just sets the brush color to the canvas background
        self.brush_color = self.bg_color

    def change_size(self, val):
        try:
            self.brush_size = int(val)
        except ValueError:
            pass

    def start_draw(self, event):
        self.last_x, self.last_y = event.x, event.y

    def draw(self, event):
        x, y = event.x, event.y
        if self.last_x is not None and self.last_y is not None:
            # create_line returns the id, store it for undo
            item = self.canvas.create_line(
                self.last_x, self.last_y, x, y,
                width=self.brush_size,
                fill=self.brush_color,
                capstyle=tk.ROUND,
                smooth=True
            )
            self.drawn_items.append(item)
        self.last_x, self.last_y = x, y

    def end_draw(self, event):
        self.last_x, self.last_y = None, None

    def clear(self):
        self.canvas.delete("all")
        self.drawn_items.clear()

    def undo(self):
        if self.drawn_items:
            last = self.drawn_items.pop()
            self.canvas.delete(last)
        else:
            messagebox.showinfo("Undo", "Nothing to undo.")

    def save(self):
        # Ask for filename
        file = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png"), ("PostScript", "*.ps")],
            title="Save your masterpiece"
        )
        if not file:
            return

        # Save canvas as postscript first (always supported)
        ps = self.canvas.postscript(colormode='color')

        # Save temporary .ps
        tmp_ps = file + ".tmp.ps"
        with open(tmp_ps, "w", encoding="utf-8") as f:
            f.write(ps)

        # Try convert with Pillow if available
        if PIL_AVAILABLE:
            try:
                # Pillow needs Ghostscript to open EPS/PS on many systems.
                img = Image.open(tmp_ps)
                # Crop to content if white border exists (optional)
                # img = img.convert("RGB")
                img.save(file, "PNG")
                os.remove(tmp_ps)
                messagebox.showinfo("Saved", f"Saved as {file}")
                return
            except Exception as e:
                # conversion failed, fall back to keeping PS
                print("Pillow conversion failed:", e)

        # If we reach here, conversion to PNG failed or Pillow not available
        fallback_name = file if file.lower().endswith(".ps") else file + ".ps"
        os.replace(tmp_ps, fallback_name)
        messagebox.showinfo("Saved (PS)", f"Pillow/ghostscript not available or conversion failed.\nSaved PostScript: {fallback_name}\nYou can convert .ps to .png with Pillow + Ghostscript or external tools.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
