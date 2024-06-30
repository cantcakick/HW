import tkinter as tk

window=tk.Tk()
canvas=tk.Canvas(window,width=640, height=480, bg='blue')
canvas.create_line()
canvas.grid(row=0)
window.mainloop()