from tkinter import *

class app:
    def __init__(self, root):
        win1 = Frame(root)
        win1.grid(row=0,column=0)

        self.variable = StringVar(win1)                               
        self.variable.set(42)
        self.type = OptionMenu(win1, self.variable,
                          "None", "Clear", "Dark", "Heavy",
                          command = self.varMenu)
        self.type.grid(row=1, column=3, sticky="nsew", padx=1, pady=1)


        self.variableunit = StringVar(win1)
        self.variableunit.set('mm')
        self.unit = OptionMenu(win1,
                          self.variableunit, "mm", "colour", "shade")
        self.unit.grid(row=1, column=5, sticky="nsew", padx=1, pady=1)

    def varMenu(self, selection):
        if selection == "Heavy":
            self.variableunit.set("colour")
            self.unit.config(state = DISABLED)
        else:
            self.variableunit.set("mm")
            self.unit.config(state = NORMAL)

root = Tk()
a = app(root)
root.mainloop()


"""from tkinter import *

INGREDIENTS = ['cheese','ham','pickle','mustard','lettuce']

def print_ingredients(*args):
   values = [(ingredient, var.get()) for ingredient, var in data.items()]
   print(values)

data = {} # dictionary to store all the IntVars

top = Tk()

mb=  Menubutton ( top, text="Ingredients", relief=RAISED )
mb.menu  =  Menu ( mb, tearoff = 0 )
mb["menu"]  =  mb.menu

for ingredient in INGREDIENTS:
    var = IntVar()
    mb.menu.add_checkbutton(label=ingredient, variable=var)
    data[ingredient] = var # add IntVar to the dictionary

btn = Button(top, text="Print", command=print_ingredients)
btn.pack()

mb.pack()

top.mainloop()"""