import tkinter as tk
def blink():
    global is_white
    if is_white:
        color='black'
    else:
        color='white'
    is_white= not is_white
    frame.config(bg=color)
    frame.after(500,blink)
def suicide():
    frame.destroy()
def flip_focus():
    if window.focus_get() is button1:
        button2.focus_set()
    else:
        button1.focus_set()
    window.after(1000,flip_focus)    

is_white=True
window=tk.Tk()
w2=tk.Tk()
frame=tk.Frame(window,width=200,height=100,bg='white')
button1=tk.Button(w2,text='First')
button1.pack()
button2=tk.Button(w2,text='Second')
button2.pack()
frame.after(500,blink)
frame.after(1000,suicide)
frame.pack()
window.mainloop()