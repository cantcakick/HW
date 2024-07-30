import tkinter as tk

def on_off():
    global button
    #state=button['text']
    state=button.cget('text') #alt method
    if state== 'ON':
        state=='OFF'
    else:
        state='ON'
    #button['text']=state
    button.config(text=state) #alt method
window=tk.Tk()
button=tk.Button(window,text='OFF',command=on_off)
button.pack()
window.mainloop()