import tkinter as tk
from tkinter import messagebox

def about_app():
    messagebox.showinfo('App',"I don't do anything")
def confirm():
    if messagebox.askyesno('','Are you sure you want to quit?'):
        window.destroy()
    
window=tk.Tk()

main_menu=tk.Menu(window)
window.config(menu=main_menu)

sub_menu_file=tk.Menu(main_menu,tearoff=0)
main_menu.add_cascade(label='File',menu=sub_menu_file,underline=0)
sub_menu_file.add_command(label='Open')
sub_menu_file.add_cascade(label='Recent Files',underline=0,menu=sub_menu_file)

for i in range(5):
    number=str(i+1)
    sub_menu_file.add_command(label=number + '.file.txt',underline=0)
    
sub_menu_file.add_separator()
sub_menu_file.add_command(label='Quit',underline=0,command=confirm)
sub_menu_help=tk.Menu(main_menu)
main_menu.add_command(label='About...',command=about_app)

window.mainloop()