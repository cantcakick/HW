import tkinter as tk
from tkinter import messagebox
def on_off():
    global switch
    if switch:
        label.unbind('<Button-1>')
    else:
        label.bind('<Button-1>',rhyme)
    switch=not switch
    
def rhyme(dummy):
    global count, words
    count+=1
    label.config(text=words[count%len(words)])
def hello(dummy):
    messagebox.showinfo('','Hi')    
switch=True
words=['Korvo','Try','Points','walrus','perfect']
count=0
window=tk.Tk()
button=tk.Button(window,text='On/Off',command=on_off)
button.pack()
label=tk.Label(window,text=words[0])
label.bind('<Button-1>',rhyme)
label.pack()
window.bind_all('<Button-1>',hello)
window.mainloop()