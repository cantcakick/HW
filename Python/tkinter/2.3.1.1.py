import tkinter as tk

def isNum(*args):
    global last_string
    string=text.get()
    if string== '' or string.isdigit():
        last_string=string
    else:
        text.set(last_string)
        
last_string=''
window=tk.Tk()
text=tk.StringVar()
entry=tk.Entry(window,textvariable=text)
text.set(last_string)
text.trace('w',isNum)
entry.pack()
entry.focus_set()
window.mainloop()