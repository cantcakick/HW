import tkinter as tk

def toString(x):
    return 'Current counter \nvalue is:\n'+ str(x)

def incr():
    global counter
    counter+=1
    text.set(toString(counter))
    
counter=0
window=tk.Tk()
button=tk.Button(window,text='Another one',command=incr)
button.pack()
text=tk.StringVar()
label=tk.Label(window,textvariable=text,height=4)
text.set(toString(counter))
label.pack()
window.mainloop()