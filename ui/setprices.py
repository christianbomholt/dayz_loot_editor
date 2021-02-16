from tkinter import *
from tkinter import _setit, messagebox
from database.dao import Dao
from utility.categories import traderCatSwitcher
from utility.exportTrader import createTrader, distribute
from utility.exportTrader import rarityForTrader
from config import ConfigManager


def set_trader_category(trader_category, subtype):
    if trader_category == "" or trader_category is None:
        trader_category = traderCatSwitcher(subtype)
    return trader_category


def create_label(root, text, row, column, sticky="w", px=5, py=5):
    Label(root, text=text).grid(row=row, column=column, sticky=sticky, padx=px, pady=py)


def set_entry_val(entry, new_val):
    entry.delete(0, END)
    entry.insert(END, str(new_val))


class TraderEditor(object):
    def __init__(self, root, selected_mods):
        self.window = Toplevel(root)
        self.window.wm_title("Set Prices for trader config")
        self.window.grab_set()
        self.selectedMods = selected_mods
        self.traderVal = []
        self.config = ConfigManager("config.xml")
        self.database = Dao(self.config.get_database())
        self.selected_trader = ""
        self.main = Frame(self.window)
        self.main.grid()
        self.__create_sub_types()
        self.__create_trader_editor(self.window)
        self.__create_trader_setting(self.window, 1, 1)
        self.subTypeListbox.bind("<<ListboxSelect>>", self.__fill_trader_window)

    def __set_selected_trader(self, value):
        self.selected_trader = value
        self.__trader__update()

    def __create_sub_types(self):
        subtypes_frame = Frame(self.main)
        subtypes_frame.grid(row=2, column=1, columnspan=1, pady=10)
        self.selected_trader = StringVar()
        traders_option_menu = OptionMenu(subtypes_frame,
                                         self.selected_trader,
                                         *self.config.get_traders(),
                                         command=self.__set_selected_trader)
        traders_option_menu.grid(row=0, column=1, sticky="w", pady=5)
        self.selected_trader.set(self.config.get_traders()[0])
        self.selected_trader = self.config.get_traders()[0]
        self.subTypeListbox = Listbox(subtypes_frame, width=35, height=30, exportselection=False)
        self.subTypeListbox.grid(row=1, column=1, sticky="ns", padx=10)
        sub_type_lst = self.database.get_tradersubtypetupl(self.selected_trader, self.selectedMods)

        for sub_type in sub_type_lst:
            if sub_type == "":
                sub_type = "UNASSIGNED"
            self.subTypeListbox.insert(END, sub_type)

    def __create_trader_editor(self, root):
        self.__fill_trader_window(root)

    def __create_trader_setting(self, root, row, column):
        radio_frame = Frame(root)
        radio_frame.grid(row=row, column=column, sticky="w", pady=5)
        modes = [("Use Rarity", "rar"), ("Use Nominal", "nom")]
        self.v = StringVar()
        self.v.set("rar")
        Radiobutton(radio_frame, text=modes[0][0], variable=self.v, value=modes[0][1]).grid(row=0, column=0)
        Radiobutton(radio_frame, text=modes[1][0], variable=self.v, value=modes[1][1]).grid(row=0, column=1)
        frame = Frame(root)
        frame.grid(row=row + 1, column=column, sticky="w", pady=5)
        self.buy_entries = self.__create_price_block(frame, "Buy Price", 0, 0)
        self.sellEntries = self.__create_price_block(frame, "Sell Price", 0, 1)
        button_frame = Frame(root)
        button_frame.grid(row=row + 2, column=column, sticky="w", pady=5)

        Button(button_frame, text="Distribute Pricing", command=self.__distribute_pricing).grid(row=0, column=0)
        Button(button_frame, text="Apply Fractions", command=self.__apply_fractions).grid(row=0, column=1)
        Button(button_frame, text="Save Changes", command=self.update).grid(row=0, column=2)
        Button(button_frame, text="Copy to Clipboard", command=self.__create_trader).grid(row=0, column=3, padx=5)

    def __trader__update(self):
        sub_type_lst = self.database.get_tradersubtypetupl(self.selected_trader, self.selectedMods)
        self.subTypeListbox.delete(0, 'end')
        for sub_type in sub_type_lst:
            if sub_type == "":
                sub_type = "UNASSIGNED"
            self.subTypeListbox.insert(END, sub_type)

    def __create_price_block(self, parent, name, row, column):
        buy_price = LabelFrame(parent, text=name)
        buy_price.grid(row=row, column=column, padx=10)
        #
        create_label(buy_price, "Minimal:", 0, 0, "w")
        create_label(buy_price, "Maximal:", 1, 0, "w")
        #
        min_val = IntVar()
        min_val.set(0)
        min_val = Entry(buy_price, textvariable=min_val)
        min_val.grid(row=0, column=1, padx=5, pady=5)
        #
        max_val = IntVar()
        max_val.set(0)
        max_val = Entry(buy_price, textvariable=max_val)
        max_val.grid(row=1, column=1, padx=5, pady=5)
        #
        if "sell" in name.lower():
            create_label(buy_price, "fraction:", 2, 0, "w")
            self.fraction = Entry(buy_price)
            self.fraction.insert(END, '1.0')
            self.fraction.grid(row=2, column=1, padx=5, pady=5)
        return min_val, max_val

    def __update_scroll_region(self, root):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def __trader_row(self, parent, name, trader_category, buy_price, sell_price, rarity, nominal, exclude):
        frame = Frame(parent)
        frame.grid(padx=5, pady=2, sticky="w")
        #
        do_exclude = IntVar()
        do_exclude.set(exclude)
        #
        name_var = StringVar()
        name_var.set(name)
        #
        trader_category_var = StringVar()
        trader_category_var.set(trader_category)
        #
        buy_price_var = StringVar()
        buy_price_var.set(buy_price)
        #
        sell_price_var = StringVar()
        sell_price_var.set(sell_price)
        #
        x_padding = 10
        Checkbutton(frame, variable=do_exclude).grid(row=0, column=0)
        name_entry = Entry(frame, textvariable=name_var, width=25)
        name_entry.grid(row=0, column=1, padx=x_padding)
        trader_cat_entry = Entry(frame, textvariable=trader_category_var, width=3)
        trader_cat_entry.grid(row=0, column=2, padx=x_padding)
        buy_price_entry = Entry(frame, textvariable=buy_price_var, width=8)
        buy_price_entry.grid(row=0, column=3, padx=x_padding)
        sell_price_entry = Entry(frame, textvariable=sell_price_var, width=8)
        sell_price_entry.grid(row=0, column=4, padx=x_padding)
        self.traderVal.append(
            ([trader_cat_entry, buy_price_entry, sell_price_entry, do_exclude], [rarity, name, nominal]))

    # def fillTraderWindow(self,parent, event):
    def __fill_trader_window(self, root):
        root = self.window
        selected_sub_type = self.subTypeListbox.get(ANCHOR)
        selected_sub_type = "" if selected_sub_type == "UNASSIGNED" else selected_sub_type
        items = self.database.get_traderitemstupl(self.selected_trader, selected_sub_type, self.selectedMods)
        height = 480
        width = 400
        self.frame = Frame(root, height=height, width=width)
        self.frame.grid_forget()
        self.traderVal = []
        self.frame.grid(row=0, column=1, sticky="nw", pady=20)
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.canvas = Canvas(self.frame, height=height, width=width)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvasFrame = Frame(self.canvas, height=height, width=width)
        self.canvas.create_window(0, 0, window=self.canvasFrame, anchor='nw')
        #
        for i in items:
            traderCat = i.get("traderCat")
            subtype = i.get("sub_type")
            traderCat = set_trader_category(traderCat, subtype)
            self.__trader_row(self.canvasFrame, i.get("name"), traderCat, i.get("buyprice"), i.get("sellprice"),
                              i.get("rarity"), i.get("nominal"), i.get("traderExclude"))
        scrollbar = Scrollbar(self.frame, orient=VERTICAL)
        scrollbar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")
        root.rowconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        self.canvasFrame.bind("<Configure>", self.__update_scroll_region)

    def __create_values(self):
        values = []
        for i in range(len(self.traderVal)):
            item = []
            for entry in self.traderVal[i][0]:
                item.append(entry.get())
            item.append(self.traderVal[i][1][0])
            item.append(self.traderVal[i][1][1])
            values.append(item)
        return values

    def update(self):
        values = self.__create_values()
        self.database.setTraderValues_fast(values)

    def __create_trader(self):
        sub_type = self.subTypeListbox.get(ANCHOR)
        items = self.__create_values()
        new_items = []
        for item in items:
            # name, traderCat, buyPrice, sellPrice, rarity
            new_item = [item[5], item[0], item[1], item[2], item[3], item[4]]
            new_items.append(new_item)
        createTrader(self.window, sub_type, new_items)

    def __apply_fractions(self):
        sel_subtype = self.subTypeListbox.get(ANCHOR)
        sel_subtype = "" if sel_subtype == "UNASSIGNED" else sel_subtype
        item = []
        trader_item = self.database.get_traderpricingtupl(self.selected_trader, sel_subtype, self.selectedMods)
        for i in trader_item:
            item.append(i)
        for item in self.traderVal:
            sell_price = int(float(item[0][1].get()) * float(self.fraction.get())) if item[0][1].get() != "-1" else -1
            set_entry_val(item[0][2], sell_price)

    def __distribute_pricing(self):
        global pricing
        rarity_is_set = True if self.v.get() == "rar" else False
        selected_subtype = self.subTypeListbox.get(ANCHOR)
        selected_subtype = "" if selected_subtype == "UNASSIGNED" else selected_subtype
        item = []
        trader_item = self.database.get_traderpricingtupl(self.selected_trader, selected_subtype, self.selectedMods)
        rarities = []
        for i in trader_item:
            item.append(i)
        # rarity, nominal
        for i in item:
            rarities.append((i[5], i[6]))
        try:
            pricing = distribute(rarities, int(self.buy_entries[0].get()), int(self.buy_entries[1].get()),
                                 int(self.sellEntries[0].get()), int(self.sellEntries[1].get()), rarity_is_set)
        except IndexError:
            windows.showError(self.window, "No rarities", "Set the rarity for your items, or use nominals")
        if len(pricing) == 2:
            for i in self.traderVal:
                set_entry_val(i[0][1], int(self.buy_entries[0].get()))
                set_entry_val(i[0][2], int(self.sellEntries[0].get()))
        else:
            buy_pricing = pricing[0]
            sell_pricing = pricing[1]
            for i in self.traderVal:
                try:
                    key_value = rarityForTrader[i[1][0]] if rarity_is_set else i[1][2]
                except KeyError:
                    key_value = 0
                print(key_value)
                set_entry_val(i[0][1], buy_pricing[key_value])
                set_entry_val(i[0][2], sell_pricing[key_value])


def test_window():
    window = Tk()
    TraderEditor(window)
    window.mainloop()