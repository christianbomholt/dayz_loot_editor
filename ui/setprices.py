from tkinter import *
from tkinter import _setit, messagebox

#import windows
# import pyperclip
from database.dao import Dao
from utility.categories import traderCatSwitcher
from utility.exportTrader import createTrader, distribute
from utility.exportTrader import rarityForTrader
from config import ConfigManager

class TraderEditor(object):
    def __init__(self, root, selectedMods):
        self.window = Toplevel(root)

        self.window.wm_title("Set Prices for trader config")
        self.window.grab_set()
        self.selectedMods = selectedMods
        self.traderVal = []
        self.config = ConfigManager("config.xml")
        self.database = Dao(self.config.get_database())
        self.seltrader = ""
        self.main = Frame(self.window)
        self.main.grid()
        self.createSubTypes("all")
        self.createTraderEditor(self.window, 0, 1)
        self.createTraderSetting(self.window, 1, 1)
        self.subTypeListbox.bind("<<ListboxSelect>>", self.fillTraderWindow)
        

    def setseltrader(self,value):
        self.seltrader = value
        self.traderupdate()

    def createSubTypes(self, seltrader):
        subtypesFrame = Frame(self.main)
        subtypesFrame.grid(row=2, column=1, columnspan=1, pady=10)

        self.seltrader = StringVar()
        self.traderSel = OptionMenu(
            subtypesFrame, self.seltrader, *self.config.get_traders(), command=self.setseltrader
        )
        self.traderSel.grid(row=0, column=1, sticky="w", pady=5)
        self.seltrader.set(self.config.get_traders()[0])
        self.seltrader = self.config.get_traders()[0]

        self.subTypeListbox = Listbox(subtypesFrame, width=35, height=30, exportselection=False)
        self.subTypeListbox.grid(row = 1, column=1, sticky="ns", padx=10)

        subTypeLst = self.database.get_tradersubtypetupl(self.seltrader,self.selectedMods)   

        for subType in subTypeLst:
            if subType == "":
                subType = "UNASSIGNED"
            self.subTypeListbox.insert(END, subType)


    def traderupdate(self):
        subTypeLst = self.database.get_tradersubtypetupl(self.seltrader,self.selectedMods)
        self.subTypeListbox.delete(0,'end')
        for subType in subTypeLst:
            if subType == "":
                subType = "UNASSIGNED"
            self.subTypeListbox.insert(END, subType)       

    def testdef(self):
        traderitem = self.database.get_traderpricingtupl(self.seltrader,"Rifles",self.selectedMods)

    def createTraderEditor(self, root, row, column):    
        self.fillTraderWindow(root)

    # name-0, subtype-1, tradercat-2, buyprice-3, sellprice, rarity, nominal, traderexclude, mod
    def setTraderCat(self,traderCat, subtype):
        if traderCat == "" or traderCat == None:
            traderCat = traderCatSwitcher(subtype)
        return traderCat

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

    def traderRow(self, parent, name, sub_type, traderCat, buyPrice, sellPrice, rarity, nominal, exclude):
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

    #def fillTraderWindow(self,parent, event):
    def fillTraderWindow(self,parent):
        root = self.window        
        selSubtype = self.subTypeListbox.get(ANCHOR)
        selSubtype = "" if selSubtype == "UNASSIGNED" else selSubtype
        items = self.database.get_traderitemstupl(self.seltrader,selSubtype,self.selectedMods)
        height = 480
        width = 400
        self.frame = Frame(root, height=height, width=width)
        self.frame.grid_forget()
        self.traderVal = []        
        self.frame.grid(row=0, column=1, sticky="nw", pady=20)
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.canv = Canvas(self.frame, height=height, width=width)
        self.canv.grid(row=0, column=0, sticky="nsew")
        self.canvFrame = Frame(self.canv, height=height, width=width)
        self.canv.create_window(0, 0, window=self.canvFrame, anchor='nw')
        
        for i in items:
            traderCat = i.get("traderCat")
            subtype = i.get("sub_type")
            traderCat = self.setTraderCat(traderCat,subtype)
            self.traderRow(self.canvFrame, i.get("name"), subtype, traderCat, i.get("buyprice"), i.get("sellprice"), i.get("rarity"), i.get("nominal"), i.get("traderExclude"))
        scrl = Scrollbar(self.frame, orient=VERTICAL)
        scrl.config(command=self.canv.yview)
        self.canv.config(yscrollcommand=scrl.set)
        scrl.grid(row=0, column=1, sticky="ns")
        root.rowconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        self.canvFrame.bind("<Configure>", self.update_scrollregion)

    def createLabel(self, root, text, row, column, sticky="w", px=5, py=5):
        Label(root, text=text).grid(row=row, column=column, sticky=sticky, padx=px, pady=py)

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
        self.database.setTraderValues_fast(values)

    def createTrader(self):
        sub_type = self.subTypeListbox.get(ANCHOR)
        items = self.createValues()
        newItems = []
        for item in items:
                        # name, traderCat, buyPrice, sellPrice, rarity
            newItem = [item[5], item[0], item[1], item[2], item[3], item[4]]
            newItems.append(newItem)
        createTrader(self.window, sub_type, newItems)

    def applyFractions(self):
        selSubtype = self.subTypeListbox.get(ANCHOR)
        selSubtype = "" if selSubtype == "UNASSIGNED" else selSubtype
        item = []
        traderitem = self.database.get_traderpricingtupl(self.seltrader,selSubtype,self.selectedMods)
        for i in traderitem:
            item.append(i)
    
        # buyprice, sellprice, tradercat, subtype, name
        for item in self.traderVal:
            sellprice = int(float(item[0][1].get()) * float(self.frac.get())) if item[0][1].get() != "-1" else -1
            self.setEntryVal(item[0][2], sellprice)


    def distributePricing(self):
        rarity_is_set = True if self.v.get() == "rar" else False
        selSubtype = self.subTypeListbox.get(ANCHOR)
        selSubtype = "" if selSubtype == "UNASSIGNED" else selSubtype
        item = []
        traderitem = self.database.get_traderpricingtupl(self.seltrader,selSubtype,self.selectedMods)
        rarities = []
        for i in traderitem:
            item.append(i)
        # rarity, nominal
        for item in item:
            rarities.append((item[5], item[6]))
            print("distributePricing  :", item[5], item[6])
        try:
            pricing = distribute(rarities, int(self.buyEntires[0].get()), int(self.buyEntires[1].get()),
                                 int(self.sellEntries[0].get()), int(self.sellEntries[1].get()), rarity_is_set)
        except IndexError:
            windows.showError(self.window, "No rarities", "Set the rarity for your items, or use nominals")

        buyPricing = pricing[0]
        sellPricing = pricing[1]

        for item in self.traderVal:
            print("DEBUG  :", item[1][1],item[1][2] )
            try:
                keyValue = rarityForTrader[item[1][0]] if rarity_is_set else item[1][2]
            except KeyError:
                pass
                """
                keyValue = 0
            self.setEntryVal(item[0][1], buyPricing[keyValue])
            self.setEntryVal(item[0][2], sellPricing[keyValue])"""

    def setEntryVal(self, entry, newVal):
        entry.delete(0, END)
        entry.insert(END, str(newVal))


def testWindow():
    window = Tk()
    TraderEditor(window)
    window.mainloop()