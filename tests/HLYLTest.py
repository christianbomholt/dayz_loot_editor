import tkinter as tk


numbers= {'one': 1, 'two': 2, 'three': 3, 'four': 4} 
colors= {'blue': 5, 'red': 6, 'green': 7, 'orange': 8, 'pink': 9, 'yellow': 10}


def set_value():    
    dd_var.set(list(numbers)[0]) 


def displayvalue(*args):
    # this is triggered each time dd_var is reset to a value
    print(args)
    print(str(dd_var.get()))


def remove_dropdown():
    drop_values.destroy()


root = tk.Tk()
root.title('Data Comparison')

frame = tk.Frame(root)
frame.grid(column=9, row=7)

dd_var = tk.StringVar(root)
set_value()
dd_var.trace_add('write', displayvalue)

drop_values = tk.OptionMenu(frame, dd_var, *numbers)
drop_values.grid(column=7, row =1)

remove_dropdown_btn = tk.Button(frame, text='update', command=remove_dropdown)
remove_dropdown_btn.grid (column= 8, row= 7)

root.mainloop()