import tkinter as tk

window = tk.Tk()
canvas=tk.Canvas(window,width=480,height=600,bg='white')
canvas.create_text(200,200,text="Insert text here...",font=("Times New Romen","20","bold"),justify=tk.CENTER,fill='blue')
button=tk.Button(window,text="Quit",command=window.destroy)
canvas.grid(row=0)
button.grid(row=1)
window.mainloop()