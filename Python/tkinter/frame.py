import tkinter as tk

window=tk.Tk()
frame_1=tk.Frame(window,width=200,height=100,bg='white')
frame_2=tk.Frame(window,width=200,height=100,bg='red')
label_frame_1=tk.LabelFrame(window,text="Frame #1",width=200,height=100,bg="blue")

frame_1.pack()
frame_2.pack()
label_frame_1.pack()
window.mainloop()