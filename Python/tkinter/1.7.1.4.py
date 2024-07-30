import tkinter as tk

window=tk.Tk()
label1=tk.Label(window,text='Manamunah')
#label1.grid(column=0,row=0)
label1.pack()
label2=tk.Label(window,text='Manamunah',font=('Times','14'))
#label2.grid(column=0,row=1)
label2.pack()
button1=tk.Button(window,text='Normal')
button1.pack()
button1.config(bg='black',fg='yellow',activebackground='green',activeforeground='red')
button1['borderwidth']=10
button1['highlightthickness']=10
button1['padx']=10
button1['pady']=5
button1['underline']=1
button2=tk.Button(window,text='New button')
#button2["anchor"] = se
#button2['width']= 20
#button2['height']=3
button2.pack()
label3=tk.Label(window,height=3,text='clock',cursor='clock')
label3.pack()
window.mainloop()