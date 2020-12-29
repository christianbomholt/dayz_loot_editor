from tkinter import *
from tkinter import _setit

#import windows
import pyperclip
from database.dao import Dao
from utility.categories import traderCatSwitcher
from utility.exportTrader import createTrader, distribute
from utility.exportTrader import rarityForTrader


class TraderEditor(object):
    def __init__(self, root, selectedMods):
        self.window = Toplevel(root)
        self.window.wm_title("Set Prices for trader config")
        self.window.grab_set()
        self.selectedMods = selectedMods
        print("DEBUG print selected mods", selectedMods)
        self.traderVal = []
    

        self.main = Frame(self.window)
        self.main.grid()

        self.createSubTypes()
        self.createTraderEditor(self.window, 0, 1, [])
        self.createTraderSetting(self.window, 1, 1)
        self.subTypeListbox.bind("<<ListboxSelect>>", self.fillTraderWindow)

        windows.center(self.window)

    def trader_loc_callback(self, *args):
        #print("DEBUG - excuting callback with self.fillTraderWindow")
        #print("DEBUG *args", *args)
        self.fillTraderWindow({"empty_event": "empty_event"})

    def createSubTypes(self):
        subtypesFrame = Frame(self.main)
        subtypesFrame.grid()
        self.subTypeListbox = Listbox(subtypesFrame, width=35, height=30, exportselection=False)
        self.subTypeListbox.grid(sticky="ns", padx=10)
        subTypes = set()

        for mod in self.selectedMods:
            print("DEBUG print mod: ",mod)
            for subtype_in_mod in Dao.getSubtypesMods(mod):
                subTypes.add(subtype_in_mod)

        for subType in sorted(subTypes):
            if subType == "":
                subType = "UNASSIGNED"

            self.subTypeListbox.insert(END, subType)

        #######################################
        traderLocFrame = Frame(self.main)
        traderLocFrame.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        Label(traderLocFrame, text="Trader Location:").grid(row=0, column=0, sticky="w")
        #
        self.traderSel = IntVar(traderLocFrame)
        self.traderSel.set(0)
        trader_choices = [0] #dao.getTraderLocs()
        #print("DEBUG trader_choices:", trader_choices, type(trader_choices))
        self.traderloc_menu = OptionMenu(traderLocFrame, self.traderSel, *trader_choices)
        self.traderloc_menu.grid(row=0, column=0, sticky="w", padx=100)
        self.traderSel.trace("w", self.trader_loc_callback)
        #######################################

    def createTraderEditor(self, root, row, column, rows):
        self.drawEditor(root, row, column, self.setTraderCat(rows))

    def setTraderCat(self, rows):
        for i in range(len(rows)):
            traderCat = rows[i][2]
            if traderCat == "" or traderCat == None:
                rows[i][2] = traderCatSwitcher(rows[i][1])

        return rows

    def drawEditor(self, root, row, column, rows):
        height = 480
        width = 400
        self.frame = Frame(root, height=height, width=width)
        self.frame.grid(row=row, column=column, sticky="nw", pady=20)
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)

        self.canv = Canvas(self.frame, height=height, width=width)
        self.canv.grid(row=0, column=0, sticky="nsew")

        self.canvFrame = Frame(self.canv, height=height, width=width)
        self.canv.create_window(0, 0, window=self.canvFrame, anchor='nw')

        ### setup seconday filtering by trader_loc here
        ### rows are already setup
        trader_loc = self.traderSel.get()
        #print("DEBUG: self.traderSel get create", trader_loc)
        if not rows:
            # rows is empty
            #print("DEBUG - empty row", rows)
            quick_subtype = None
            trader_filtered_rows = rows
        else:
            quick_subtype = rows[0][1]
            trader_filter_reflist = dao.getItemDetailsByTraderLoc(subtype=quick_subtype, trader_loc=trader_loc)
            #print("DEBUG: trader_filter_reflist ", trader_filter_reflist)
            trader_filtered_rows = []
            for item in rows:
                if item[0] in trader_filter_reflist:
                    trader_filtered_rows.append(item)

        for item in trader_filtered_rows:
            #print("DEBUG item", item)
            self.traderRow(self.canvFrame, *item)

        scrl = Scrollbar(self.frame, orient=VERTICAL)
        scrl.config(command=self.canv.yview)
        self.canv.config(yscrollcommand=scrl.set)
        scrl.grid(row=0, column=1, sticky="ns")

        root.rowconfigure(row, weight=1)
        root.columnconfigure(column, weight=1)

        self.canvFrame.bind("<Configure>", self.update_scrollregion)

    def createTraderSetting(self, root, row, column):

        radioFrame = Frame(root)
        radioFrame.grid(row=row, column=column, sticky="w", pady=5)

        MODES = [("Use Rarity", "rar"), ("Use Nominal", "nom")]
        self.v = StringVar()
        self.v.set("rar")

        Radiobutton(radioFrame, text=MODES[0][0], variable=self.v, value=MODES[0][1]).grid(row=0, column=0)
        Radiobutton(radioFrame, text=MODES[1][0], variable=self.v, value=MODES[1][1]).grid(row=0, column=1)

        frame = Frame(root)
        frame.grid(row=row + 1, column=column, sticky="w", pady=5)

        self.buyEntires = self.createPriceBlock(frame, "Buy Price", 0, 0)
        self.sellEntries = self.createPriceBlock(frame, "Sell Price", 0, 1)
        buttonFrame = Frame(root)
        buttonFrame.grid(row=row + 2, column=column, sticky="w", pady=5)

        Button(buttonFrame, text="Distribute Pricing", command=self.distributePricing).grid(row=0, column=0)
        Button(buttonFrame, text="Apply Fractions", command=self.applyFractions).grid(row=0, column=1)
        Button(buttonFrame, text="Save Changes", command=self.update).grid(row=0, column=2)
        Button(buttonFrame, text="Copy to Clipboard", command=self.createTrader).grid(row=0, column=3, padx=5)


    def createPriceBlock(self, parent, name, row, column):
        buyPrice = LabelFrame(parent, text=name)
        buyPrice.grid(row=row, column=column, padx=10)

        self.createLabel(buyPrice, "Minimal:", 0, 0, "w")
        self.createLabel(buyPrice, "Maximal:", 1, 0, "w")
        self.min = IntVar()
        self.min.set(0)
        min = Entry(buyPrice, textvariable=self.min)
        min.grid(row=0, column=1, padx=5, pady=5)

        self.max = IntVar()
        self.max.set(0)
        max = Entry(buyPrice, textvariable=self.max)
        max.grid(row=1, column=1, padx=5, pady=5)

        if "sell" in name.lower():
            self.createLabel(buyPrice, "fraction:", 2, 0, "w")
            self.frac = Entry(buyPrice)
            self.frac.insert(END, '1.0')
            self.frac.grid(row=2, column=1, padx=5, pady=5)

        return (min, max)

    def update_scrollregion(self, event):
        self.canv.configure(scrollregion=self.canv.bbox("all"))

    def traderRow(self, parent, name, subtype, traderCat, buyPrice, sellPrice, rarity, nominal, exclude):
        frame = Frame(parent)
        frame.grid(padx=5, pady=2, sticky="w")

        doExclude = IntVar()
        doExclude.set(exclude)

        nameVar = StringVar()
        nameVar.set(name)

        traderCatVar = StringVar()
        traderCatVar.set(traderCat)

        buyPriceVar = StringVar()
        buyPriceVar.set(buyPrice)

        sellPriceVar = StringVar()
        sellPriceVar.set(sellPrice)

        xpad = 10

        Checkbutton(frame, variable=doExclude).grid(row=0, column=0)
        nameEntry = Entry(frame, textvariable=nameVar, width=25)
        nameEntry.grid(row=0, column=1, padx=xpad)
        traderCatEntry = Entry(frame, textvariable=traderCatVar, width=3)
        traderCatEntry.grid(row=0, column=2, padx=xpad)
        buyPriceEntry = Entry(frame, textvariable=buyPriceVar, width=8)
        buyPriceEntry.grid(row=0, column=3, padx=xpad)
        sellPriceEntry = Entry(frame, textvariable=sellPriceVar, width=8)
        sellPriceEntry.grid(row=0, column=4, padx=xpad)

        self.traderVal.append(([traderCatEntry, buyPriceEntry, sellPriceEntry, doExclude], [rarity, name, nominal]))

    def clearTraderWindow(self):
        self.frame.grid_forget()

        self.traderVal = []

    def refresh_tradersel(self, new_locs):
        # Reset var and delete all old options
        current_tradersel = self.traderSel.get()
        self.traderloc_menu['menu'].delete(0, 'end')
        # Insert list of new options (tk._setit hooks them up to var)
        #new_locs = (1, 2 , 3)
        for choice in new_locs:
            self.traderloc_menu['menu'].add_command(label=choice, command=_setit(self.traderSel, choice))
        if current_tradersel in new_locs:
            self.traderSel.set(current_tradersel)
        else:
            self.traderSel.set(0)

    def fillTraderWindow(self, event):
        self.clearTraderWindow()
        selSubtype = self.subTypeListbox.get(ANCHOR)
        selSubtype = "" if selSubtype == "UNASSIGNED" else selSubtype

        self.current_selSubtype = selSubtype
        trader_subtype_choices = dao.getTraderLocsBySubtype(subtype=selSubtype)
        self.refresh_tradersel(new_locs=trader_subtype_choices)

        itemsOfSubtype = dao.getSubtypeForTrader(selSubtype)
        itemsOfSubtypeOfSelectedMods = []

        for item in itemsOfSubtype:
            if item[-1] in self.selectedMods:
                itemsOfSubtypeOfSelectedMods.append(item[:-1])

        self.createTraderEditor(self.window, 0, 1, itemsOfSubtypeOfSelectedMods)

    def createLabel(self, root, text, row, column, sticky="w", px=5, py=5):
        Label(root, text=text).grid(row=row, column=column, sticky=sticky, padx=px, pady=py)

    # traderCat, buyprice, sellprice, traderExclude, rarity, name
    def createValues(self):
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
        values = self.createValues()
        dao.setSubtypeForTrader(values)

    def createTrader(self):
        subtype = self.subTypeListbox.get(ANCHOR)
        items = self.createValues()
        newItems = []
        for item in items:
            newItem = [item[5], item[0], item[1], item[2], item[3], item[4]]
            newItems.append(newItem)
        # name, traderCat, buyPrice, sellPrice, rarity
        createTrader(self.window, subtype, newItems)

    def applyFractions(self):
        selSubtype = self.subTypeListbox.get(ANCHOR)
        selSubtype = "" if selSubtype == "UNASSIGNED" else selSubtype
        # name, subtype, tradercat, buyprice, sellprice, rarity, nominal, traderexclude
        itms = dao.getSubtypeForTrader(selSubtype)

        # buyprice, sellprice, tradercat, subtype, name
        for item in self.traderVal:
            sellprice = int(float(item[0][1].get()) * float(self.frac.get())) if item[0][1].get() != "-1" else -1
            self.setEntryVal(item[0][2], sellprice)


    def distributePricing(self):
        rarity_is_set = True if self.v.get() == "rar" else False
        selSubtype = self.subTypeListbox.get(ANCHOR)
        selSubtype = "" if selSubtype == "UNASSIGNED" else selSubtype

        # name, subtype, tradercat, buyprice, sellprice, rarity, nominal, traderexclude
        itemsOfSubtype = dao.getSubtypeForTrader(selSubtype)
        rarities = []

        # rarity, nominal
        for item in itemsOfSubtype:
            rarities.append((item[5], item[6]))
        try:
            pricing = distribute(rarities, int(self.buyEntires[0].get()), int(self.buyEntires[1].get()),
                                 int(self.sellEntries[0].get()), int(self.sellEntries[1].get()), rarity_is_set)
        except IndexError:
            windows.showError(self.window, "No rarities", "Set the rarity for your items, or use nominals")

        buyPricing = pricing[0]
        sellPricing = pricing[1]

        for item in self.traderVal:
            try:
                keyValue = rarityForTrader[item[1][0]] if rarity_is_set else item[1][2]
            except KeyError:
                keyValue = 0
            self.setEntryVal(item[0][1], buyPricing[keyValue])
            self.setEntryVal(item[0][2], sellPricing[keyValue])

    def setEntryVal(self, entry, newVal):
        entry.delete(0, END)
        entry.insert(END, str(newVal))


def testWindow():
    window = Tk()
    TraderEditor(window)
    window.mainloop()
