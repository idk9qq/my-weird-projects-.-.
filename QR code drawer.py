import tkinter as tk
from tkinter import ttk, messagebox

class QRDrawer:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Drawer")
        
        # Version selection
        ttk.Label(root, text="QR Version (1-10):").grid(row=0, column=0, padx=5, pady=5)
        self.version_var = tk.IntVar(value=1)
        self.version_combo = ttk.Combobox(root, textvariable=self.version_var, values=list(range(1,11)), width=5)
        self.version_combo.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(root, text="Create Grid", command=self.create_grid).grid(row=0, column=2, padx=5, pady=5)
        
        # Canvas for drawing
        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        self.grid = []
        self.buttons = []
        
        # Export button
        ttk.Button(root, text="Export 0s/1s", command=self.export_grid).grid(row=2, column=0, columnspan=3, pady=10)

    def create_grid(self):
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        self.grid.clear()
        self.buttons.clear()
        
        version = self.version_var.get()
        size = 21 + (version - 1) * 4  # QR code size formula
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        
        for r in range(size):
            row_buttons = []
            for c in range(size):
                btn = tk.Button(self.canvas_frame, width=2, height=1, bg="white")
                btn.grid(row=r, column=c)
                btn.config(command=lambda r=r, c=c: self.toggle_cell(r,c))
                row_buttons.append(btn)
            self.buttons.append(row_buttons)
    
    def toggle_cell(self, r, c):
        self.grid[r][c] = 1 - self.grid[r][c]  # Toggle 0<->1
        self.buttons[r][c].config(bg="black" if self.grid[r][c] else "white")
    
    def export_grid(self):
        # Show grid in console
        for row in self.grid:
            print("".join(map(str,row)))
        messagebox.showinfo("Exported", "Grid exported to console!")

if __name__ == "__main__":
    root = tk.Tk()
    app = QRDrawer(root)
    root.mainloop()
