import tkinter as tk

def r_observer(*args):
    print('Read')
    
def w_observer(*args):
    print('Write')
    
window=tk.Tk()
variable=tk.StringVar()
variable.set('abcdefg')
r_obsid=variable.trace('r',r_observer)
w_obsid=variable.trace('w',w_observer)
variable.set(variable.get()+'H')
variable.trace_vdelete('r',r_obsid)
variable.set(variable.get()+'e')
variable.trace_vdelete('w',w_obsid)
print(variable.get())