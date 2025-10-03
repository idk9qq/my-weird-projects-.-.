import tkinter as tk
root = tk.Tk()

#screen resolution
root.title("quirky calculator")
root.geometry("300x400")
root.resizable(True, True)

entry = tk.Entry(root, width=16, font=("Arial", 24), borderwidth=2, relief="solid")
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

def click(number):
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, str(current) + str(number))

def clear():
    entry.delete(0, tk.END)

def calculate():
    try:
        result = eval(entry.get())
        entry.delete(0, tk.END)
        entry.insert(0, str(result))
    except:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")

buttons = [
    ('7',1,0), ('8',1,1), ('9',1,2), ('/',1,3),
    ('4',2,0), ('5',2,1), ('6',2,2), ('*',2,3),
    ('1',3,0), ('2',3,1), ('3',3,2), ('-',3,3),
    ('0',4,0), ('.',4,1), ('=',4,2), ('+',4,3),
    ('C',5,0)
]

for (text, row, col) in buttons:
    if text == "=":
        tk.Button(root, text=text, width=5, height=2, font=("Arial", 18), command=calculate).grid(row=row, column=col)
    elif text == "C":
        tk.Button(root, text=text, width=5, height=2, font=("Arial", 18), command=clear).grid(row=row, column=col)
    else:
        tk.Button(root, text=text, width=5, height=2, font=("Arial", 18), command=lambda t=text: click(t)).grid(row=row, column=col)
        # No additional code is needed here. All widgets and logic are already set up above.
root.mainloop()