import tkinter as tk
from tkinter import messagebox
def select():
    messagebox.showinfo('info','details')

window=tk.Tk()
button1=tk.Button(window,text='Show info',command=select)
button1.pack()

window.mainloop()