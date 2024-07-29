import tkinter as tk
from tkinter import messagebox
def d():
    replay=messagebox.askquestion("Quit?","Are you sure?")
    if replay=='yes':
        s.destroy()
        l.destroy()
        g.destroy()
    
s=tk.Tk()
s.title("Sky")
l=tk.Tk()
l.title('Ground')
g=tk.Tk()
g.title('Sea')
button=tk.Button(s,text="Bye!",command=d,activeforeground='black',activebackground='green')
button.place(x=10,y=10,width=300)
button2=tk.Button(s,text="Button 2")
button2.place(x=40,y=50)
button3=tk.Button(l,text="Button 3",bg='red',fg='white')
button3.grid(row=3,column=3,columnspan=3)
button4=tk.Button(g,text='button 4')
button4.pack()
button5=tk.Button(g,text='button 5')
button5.pack(side=tk.RIGHT, fill=tk.Y)
s.mainloop()
