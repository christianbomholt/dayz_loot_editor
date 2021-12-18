from tkinter import Tk, Menu, IntVar, Frame, Label, StringVar, Entry, Listbox, END, OptionMenu, Checkbutton, Button, Radiobutton
from tkinter import ttk, VERTICAL, HORIZONTAL, LabelFrame, Tcl, simpledialog

from sqlalchemy.sql.expression import column, or_
from config import ConfigManager
import os.path
from database.dao import Dao
from model.item import Item, Ammobox, init_database
from ui.db import DB
from ui.linkitems import LinkItem
from ui.new_items import NewItems
from ui.setprices import TraderEditor
from xml_manager.xml_writer import XMLWriter
import tkinter.filedialog as filedialog
import webbrowser
import time
import re
import json
# from utility.combo_box_manager import ComboBoxManager
from utility import assign_rarity, distribute_nominal, column_definition, categoriesDict, categoriesNamalskDict, distribute_mags_and_bullets, apipush, apipull, exportSpawnable, writeToJSONFile


class GUI(object):
    def __init__(self, main_container: Tk):
        #
        self.config = ConfigManager("config.xml")
        self.database = Dao(self.config.get_database())
        self.database.upgradeDB()
        self.selected_mods = []
        self.gridItems = []
        #
        self.window = main_container
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        self.menu_bar = Menu(self.window)
        self.moddict = {}
        self.modcount = 0
        self.moddlist = []
        self.totalWeaponDisplayed = IntVar()
        self.totalNumDisplayed = IntVar()
        self.nomVars = []
        self.weaponNomTypes = {"ranged": 0, "ammo": 0,
                               "optic": 0, "mag": 0, "attachment": 0}
        self.distributorValue = StringVar()
        self.weapondistributorValue = StringVar()
        self.searchName = StringVar()
        self.worldName = StringVar()
        self.worldName.set("world")
        #
        self.__create_menu_bar()
        self.__create_entry_frame()
        self.__create_tree_view()
        self.__create_side_bar()
        self.__initiate_items()
        self.__create_nominal_info()
        self.makeExpansionDir()
        #
        self.tree.bind("<ButtonRelease-1>", self.__fill_entry_frame)
        self.window.wm_title("CE-Editor v0.11.1 - " + self.config.get_database() +
                             " used for maptype: " + self.database.get_mapselectValue(1).mapselectvalue)

    def initializeapp(self):
        self.__create_tree_view()
        self.__create_side_bar()
        self.database = Dao(self.config.get_database())
        items = self.database.session.query(Item).filter(
            Item.mod.in_(self.selected_mods))
        self.gridItems = items
        self.__populate_items(self.gridItems)
        self.__initiate_items()
        self.__create_nominal_info()
        self.window.wm_title(
            "CE-Editor v0.11.1  UPDATED - fresh database - restart to see the right map")
        self.makeExpansionDir()

    def deselectAllMods(self):
        for k in self.moddict:
            self.moddict[k].set(0)
        self.__selectmodsfunction___()

    def selectAllMods(self):
        for k in self.moddict:
            self.moddict[k].set(1)
        self.__selectmodsfunction___()

    def initAllMods(self, menu):
        for mod in self.database.get_all_types("mod"):
            if mod != "all":
                self.modcount += 1
                int_var = IntVar(value=1)
                menu.add_checkbutton(
                    label=mod, variable=int_var, command=self.__selectmodsfunction___)
                self.moddict[mod] = int_var
                self.selected_mods.append(mod)

    def makeExpansionDir(self):
        try:
            os.mkdir("Expansion")
            os.mkdir("Expansion/Traders")
            os.mkdir("Expansion/TraderZones")
            os.mkdir("Expansion/Market")
        except Exception:
            pass

    def updateAllMods(self, menu):

        for i in range(self.modcount+3):
            if i > 2:
                menu.delete(i)
        for mod in self.database.get_all_types("mod"):
            if mod != "all":
                int_var = IntVar(value=1)
                menu.add_checkbutton(
                    label=mod, variable=int_var, command=self.__selectmodsfunction___)
                self.moddict[mod] = int_var
                self.selected_mods.append(mod)

    def __create_menu_bar(self):
        # file menus builder
        file_menu = Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Setup Database",
                              command=self.__open_db_window)
        file_menu.add_command(label="Import attachfile",
                              command=self.__import_link_window)
        file_menu.add_separator()
        file_menu.add_command(
            label="Add Items", command=self.__open_items_window)
        file_menu.add_separator()
        file_menu.add_command(label="Export XML File",
                              command=self.export_xml_normal)
        file_menu.add_command(label="Export Namalsk XML File",
                              command=self.export_xml_Namalsk)
        file_menu.add_separator()
        file_menu.add_command(label="Export Spawnable Types",
                              command=self.writespawnabletypes)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.window.destroy)
# database menus builder

# help menus builder
        help_menu = Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="Watch the video....",
                              command=self.demovideo)

# tools menus builder
        tools_menu = Menu(self.menu_bar, tearoff=0)
        tools_menu.add_command(
            label="Derive types and subtypes", command=self.derivetypessubtypes)
        tools_menu.add_command(
            label="Assign Rarity from nominal", command=self.func2assign_raritiy)
        tools_menu.add_separator()
        tools_menu.add_command(
            label="Dump database to sql file", command=self.dump2sql)
        tools_menu.add_separator()
        tools_menu.add_command(
            label="Derive ammobox table", command=self.deriveammobox)
        tools_menu.add_command(
            label="Distribute gun,mag and bullet", command=self.testdist)
        # tools_menu.add_command(label="TestFunction for (Dev)", command=self.testfunction)
        # tools_menu.add_command(label="APIPull (Dev)", command=self.apipull)
        # tools_menu.add_command(label="APIPush (Dev)", command=self.apipush)

# initializing mods menu
        self.mods_menu = Menu(self.menu_bar, tearoff=0)
        self.mods_menu.add_command(
            label="Deselect All", command=self.deselectAllMods)
        self.mods_menu.add_command(
            label="Select All", command=self.selectAllMods)
        self.mods_menu.add_separator()
        self.initAllMods(self.mods_menu)


# building menu bar
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        self.menu_bar.add_cascade(label="Mods In Use", menu=self.mods_menu)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)
        self.menu_bar.add_cascade(label="Tools", menu=tools_menu)

# configuring menu bar
        self.window.config(menu=self.menu_bar)

    def export_xml_normal(self):
        self.__export_xml("Normal")

    def export_xml_Namalsk(self):
        self.__export_xml("Namalsk")

# Create Left side entry frame  *************************************************
    def __create_entry_frame(self):
        self.entryFrameHolder = Frame(self.window)
        self.entryFrameHolder.grid(row=0, column=0, sticky="nw")
        self.entryFrame = Frame(self.entryFrameHolder)
        self.entryFrame.grid(padx=8, pady=6)
        # labels
        Label(self.entryFrame, text="Name").grid(
            row=0, column=0, sticky="w", pady=5)
        Label(self.entryFrame, text="Nominal").grid(
            row=1, column=0, sticky="w", pady=5)
        Label(self.entryFrame, text="Min").grid(
            row=2, column=0, sticky="w", pady=5)
        Label(self.entryFrame, text="QMin").grid(
            row=3, column=0, sticky="w", pady=5)
        Label(self.entryFrame, text="QMax").grid(
            row=4, column=0, sticky="w", pady=5)
        Label(self.entryFrame, text="Restock").grid(
            row=5, column=0, sticky="w", pady=5)
        Label(self.entryFrame, text="Lifetime").grid(
            row=6, column=0, sticky="w", pady=5)
        Label(self.entryFrame, text="Usages").grid(
            row=7, column=0, sticky="w", pady=5)
        Label(self.entryFrame, text="Tiers").grid(
            row=8, column=0, sticky="w", pady=5)
        Label(self.entryFrame, text="Category").grid(
            row=9, column=0, sticky="w", pady=5)
        Label(self.entryFrame, text="Type").grid(
            row=10, column=0, sticky="w", pady=5)
        Label(self.entryFrame, text="Sub Type").grid(
            row=11, column=0, sticky="w", pady=5)
        Label(self.entryFrame, text="Rarity").grid(
            row=12, column=0, sticky="w", pady=5)
        Label(self.entryFrame, text="Mod").grid(
            row=13, column=0, sticky="w", pady=5)
        Label(self.entryFrame, text="Trader").grid(
            row=14, column=0, sticky="w", pady=5)
        # input variables
        self.id = IntVar()
        self.name = StringVar()
        self.nominal = IntVar()
        self.min = IntVar()
        self.qmin = IntVar()
        self.qmax = IntVar()
        self.restock = IntVar()
        self.lifetime = IntVar()
        self.usages = StringVar()
        self.tiers = StringVar()
        self.cat_type = StringVar()
        self.item_type = StringVar()
        self.sub_type = StringVar()
        self.rarity = StringVar()
        self.mod = StringVar()
        self.trader = StringVar()
        self.dynamic_event = IntVar()
        self.count_in_cargo = IntVar()
        self.count_in_hoarder = IntVar()
        self.count_in_player = IntVar()
        self.count_in_map = IntVar()
        # form fields
        self.nameField = Entry(self.entryFrame, textvariable=self.name)
        self.nameField.grid(row=0, column=1, sticky="w")
        self.nominalField = Entry(self.entryFrame, textvariable=self.nominal)
        self.nominalField.grid(row=1, column=1, sticky="w")
        self.minField = Entry(self.entryFrame, textvariable=self.min)
        self.minField.grid(row=2, column=1, sticky="w")
        self.qminField = Entry(self.entryFrame, textvariable=self.qmin)
        self.qminField.grid(row=3, column=1, sticky="w")
        self.qmaxField = Entry(self.entryFrame, textvariable=self.qmax)
        self.qmaxField.grid(row=4, column=1, sticky="w")
        self.restockField = Entry(self.entryFrame, textvariable=self.restock)
        self.restockField.grid(row=5, column=1, sticky="w")
        self.lifetimeField = Entry(self.entryFrame, textvariable=self.lifetime)
        self.lifetimeField.grid(row=6, column=1, sticky="w")
        self.usagesListBox = Listbox(
            self.entryFrame,
            height=4,
            selectmode="multiple",
            exportselection=False,
        )
        self.usagesListBox.grid(row=7, column=1, pady=5, sticky="w")
        usages = self.config.get_usages()
        for i in usages:
            self.usagesListBox.insert(END, i)

        self.tiersListBox = Listbox(
            self.entryFrame,
            height=4,
            selectmode="multiple",
            exportselection=False,
        )
        self.tiersListBox.grid(row=8, column=1, pady=5, sticky="w")
        tiers = self.config.get_tiers()
        for i in tiers:
            self.tiersListBox.insert(END, i)

        self.cat_typeOption = OptionMenu(
            self.entryFrame, self.cat_type, *
            self.database.get_all_types("cat_type")[:-1]
        )
        self.cat_typeOption.grid(row=9, column=1, sticky="w", pady=5)

        self.itemtypeAutoComp = ttk.Combobox(
            self.entryFrame, textvariable=self.item_type, values=self.database.get_all_types(
                "item_type")[:-1]
        )
        self.itemtypeAutoComp.grid(row=10, column=1, sticky="w", pady=5)

        self.subtypeAutoComp = ttk.Combobox(
            self.entryFrame, textvariable=self.sub_type, values=self.database.get_all_types("sub_type")[
                :-1]
        )
        self.subtypeAutoComp .grid(row=11, column=1, sticky="w", pady=5)

        self.rarityOption = OptionMenu(
            self.entryFrame, self.rarity, *self.config.get_rarities()
        )
        self.rarityOption.grid(row=12, column=1, sticky="w", pady=5)

        self.modOption = OptionMenu(
            self.entryFrame, self.mod, *self.database.get_all_types("mod")[:-1]
        )
        self.modOption.grid(row=13, column=1, sticky="w", pady=5)

        self.traderOption = OptionMenu(
            self.entryFrame, self.trader, *self.config.get_traders()
        )
        self.traderOption.grid(row=14, column=1, sticky="w", pady=5)

        self.checkBoxFrame = Frame(self.entryFrameHolder)
        self.checkBoxFrame.grid(row=1, column=0, columnspan=2, sticky="w")
        self.dynamic_event_check = Checkbutton(
            self.checkBoxFrame, text="Dynamic Event", variable=self.dynamic_event, onvalue=1, offvalue=0
        )
        self.dynamic_event_check.grid(row=0, column=0, sticky="w")

        self.count_in_hoarder_check = Checkbutton(
            self.checkBoxFrame, text="Count in Hoarder", variable=self.count_in_hoarder, onvalue=1, offvalue=0
        )
        self.count_in_hoarder_check.grid(row=1, column=0, sticky="w")

        self.count_in_cargo_check = Checkbutton(
            self.checkBoxFrame, text="Count in Cargo", variable=self.count_in_cargo, onvalue=1, offvalue=0
        )
        self.count_in_cargo_check.grid(row=2, column=0, sticky="w")

        self.count_in_player_check = Checkbutton(
            self.checkBoxFrame, text="Count in Player", variable=self.count_in_player, onvalue=1, offvalue=0
        )
        self.count_in_player_check.grid(row=3, column=0, sticky="w")

        self.count_in_map_check = Checkbutton(
            self.checkBoxFrame, text="Count in Map", variable=self.count_in_map, onvalue=1, offvalue=0
        )
        self.count_in_map_check.grid(row=4, column=0, sticky="w")

        Button(
            self.checkBoxFrame, text="Update", width=8, command=self.__update_item
        ).grid(row=5, column=0, pady=5, sticky="w")

        Button(
            self.checkBoxFrame, text="Delete", width=8, command=self.__delete_item
        ).grid(row=5, column=1, pady=5, sticky="w")

# **********************Create tree view ************************************************************
#

    def fixed_map(self, style, option):
        return [elm for elm in style.map("Treeview", query_opt=option)
                if elm[:2] != ("!disabled", "!selected")]

    def __create_tree_view(self):
        style = ttk.Style()
        style.configure('Treeview', background='#97FFFF', foreground='black')

        self.treeFrame = Frame(self.window)
        self.treeFrame.grid(row=0, column=1, sticky="nsew")
        self.treeFrame.grid_rowconfigure(0, weight=1)
        self.treeFrame.grid_columnconfigure(1, weight=1)

        self.tree = ttk.Treeview(self.treeFrame, columns=[col.get(
            "text") for col in column_definition], height=40)
        style.map("Treeview",
                  foreground=self.fixed_map(style, "foreground"),
                  background=self.fixed_map(style, "background"))
        for col in column_definition:
            self.tree.heading(
                col.get("col_id"),
                text=col.get("text"),
                command=lambda _col=col.get("text"): self.tree_view_sort_column(
                    self.tree, _col, False
                ),
            )
            self.tree.column(
                col.get("col_id"),
                width=col.get("width"),
                stretch=col.get("stretch")
            )
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree.heading('#0', text='ID')

        self.tree.column('#0', width="60", stretch="NO")
        self.treeView = self.tree
        vertical = ttk.Scrollbar(self.treeFrame, orient=VERTICAL)
        horizontal = ttk.Scrollbar(self.treeFrame, orient=HORIZONTAL)
        vertical.grid(row=0, column=1, sticky="ns")
        horizontal.grid(row=1, column=0, sticky="we")
        self.tree.config(yscrollcommand=vertical.set)
        self.tree.config(xscrollcommand=horizontal.set)
        vertical.config(command=self.tree.yview)
        horizontal.config(command=self.tree.xview)

    def __create_side_bar(self):
        self.filterFrameHolder = Frame(self.window)
        self.filterFrameHolder.grid(row=0, column=2, sticky="n")
        self.filterFrame = LabelFrame(
            self.filterFrameHolder, width=14, text="Filter")
        self.filterFrame.grid(row=1, column=1, pady=5)
        Label(self.filterFrame, text="Category").grid(
            row=1, column=0, sticky="w")
        Label(self.filterFrame, text="Item type").grid(
            row=2, column=0, sticky="w")
        Label(self.filterFrame, text="Sub type").grid(
            row=3, column=0, sticky="w")

        self.__create_distribution_block()
        # self.__create_weapon_distribution_block()

# Category
        self.cat_type_for_filter = StringVar()
        self.cat_type_for_filter.set("all")
        OptionMenu(
            self.filterFrame, self.cat_type_for_filter, *self.database.get_all_types("cat_type"), command=self.__CatFilter__
        ).grid(row=1, column=1,  sticky="w", padx=5)

# Item_type
        self.type_for_filter = StringVar()
        self.type_for_filter.set("all")
        OptionMenu(
            self.filterFrame, self.type_for_filter, *self.database.get_all_types("item_type"), command=self.__TypeFilter__
        ).grid(row=2, column=1, sticky="w", padx=5)

# Sub_type
        self.sub_type_for_filter = StringVar()
        self.sub_type_for_filter.set("all")
        OptionMenu(
            self.filterFrame, self.sub_type_for_filter, *self.database.get_all_types("sub_type"), command=self.__SubTypeFilter__
        ).grid(row=3, column=1, sticky="w", padx=5)

# Usage_Flag
        self.usage_for_filter = StringVar(
            value=self.database.get_all_usage("usage"))

        self.LB_usage_filter = Listbox(
            self.filterFrame, height=4, listvariable=self.usage_for_filter, selectmode="extended", exportselection=False
        )
        self.LB_usage_filter.grid(row=4, columnspan=2, sticky="w", padx=5)

        Button(
            self.filterFrame, text="Filter", width=12, command=self.__filter_items
        ).grid(row=5, columnspan=2, pady=5, padx=10, sticky="nesw")

# Search like name
        Entry(self.filterFrame, textvariable=self.searchName, width=14).grid(
            row=6, columnspan=2, pady=5, padx=10, sticky="nesw")
        Button(
            self.filterFrame,
            text="Search like Name",
            width=14,
            command=self.__search_like_name,
        ).grid(row=7, columnspan=2, pady=5, padx=10, sticky="nesw")

#
# This is were we have the test button
#
        Button(
            self.filterFrame,
            text="Trader Editor",
            width=14,
            command=self.openTraderEditor,
        ).grid(row=8, columnspan=2, pady=5, padx=10, sticky="nesw")

        Entry(self.filterFrame, textvariable=self.worldName, width=14).grid(
            row=9, columnspan=2, pady=5, padx=10, sticky="nesw")

        Button(
            self.filterFrame,
            text="Expansion Trader",
            width=14,
            command=self.expansionTrader,
        ).grid(row=10, columnspan=2, pady=5, padx=10, sticky="nesw")

        Button(
            self.filterFrame,
            text="Donate !",
            width=14,
            command=self.donate,
        ).grid(row=11, columnspan=2, pady=5, padx=10, sticky="nesw")


# Normal Distribution block

    def __create_distribution_block(self):
        self.distribution = LabelFrame(
            self.filterFrameHolder, width=14, text="Nominal Distribution")
        self.distribution.grid(row=2, column=1, pady=5)
        Label(self.distribution, text="By Displayed Items").grid(
            row=0, columnspan=2)
        Label(self.distribution, text="Target Nominal").grid(
            row=1, columnspan=2)
        self.desiredNomEntry = Entry(
            self.distribution, textvariable=self.totalNumDisplayed, width=14
        ).grid(row=2, columnspan=2, pady=7)
        self.distributorValue.set("Use Rarity")
        Radiobutton(self.distribution, text="Use Rarity", variable=self.distributorValue,
                    value="Use Rarity") .grid(row=3, column=0, sticky="w")
        Radiobutton(self.distribution, text="Use Nominal", variable=self.distributorValue,
                    value="Use Nominal").grid(row=4, column=0, sticky="w")
        Button(
            self.distribution, text="Distribute", width=12, command=self.__distribute_nominal
        ).grid(row=5, columnspan=2, pady=10)

    def readexpansionworld(self, newworld):
        try:
           # with open("./Expansion/TraderZones/World.json") as f:
            with open(f"./Expansion/TraderZones/{newworld}.json") as f:

                world = json.load(f)
            return world
        except:
            world = dict()
            world['m_Version'] = 4
            world['m_FileName'] = newworld
            world['m_ZoneName'] = newworld
            world['DisplayName'] = newworld + " Trading Zone"
            world['Position'] = [7500.0, 0.0, 7500.0]
            world['Radius'] = 50000.0
            world["Stock"] = dict()
            writeToJSONFile('./Expansion/TraderZones', newworld, world)
            return world

    def expansionTrader(self):
        newworld = str(self.worldName.get()).lower()
        world = self.readexpansionworld(newworld)
        TRADER_NAME = simpledialog.askstring(
            title="Trader Name", prompt="What's the name of the Trader?: ")
        trader = dict()
        trader['m_Version'] = 4
        trader['m_FileName'] = TRADER_NAME.upper()
        trader['TraderName'] = TRADER_NAME.upper()
        trader['DisplayName'] = "#STR_EXPANSION_MARKET_"+TRADER_NAME.upper()
        trader['Currencies'] = ["expansiongoldbar", "expansiongoldnugget",
                                "expansionsilverbar", "expansionsilvernugget"]
        # trader['Items'] = []

        trader['Items'] = dict()
        to_append = dict()
        to_append["Stock"] = dict()
        for items in self.treeView.selection():
            item = self.treeView.item(items)
            item_name = (item['values'][0])

            trader['Items'].update({item_name: 1})
            to_append["Stock"].update({item_name: 250})
        writeToJSONFile('./Expansion/Traders', TRADER_NAME.upper(), trader)
        world["Stock"].update(to_append["Stock"])
        writeToJSONFile('./Expansion/TraderZones', newworld, world)

    def donate(self):
        new = 2
        url = "https://www.paypal.com/paypalme/Luskerne"
        webbrowser.open(url, new=new)

    def demovideo(self):
        new = 2
        url = "https://youtu.be/3Jxva7KCNSk"
        webbrowser.open(url, new=new)

    def dump2sql(self):
        self.database.sql_dbDump()

    def testfunction(self):
        print("DEBUG  :", self.database.getNominalByCat(
            self.gridItems, "weapons"))

    def apipull(self):
        apipull(self.database.session)

    def apipush(self):
        apipush(self.database.session)

    def testdist(self):
        self.deriveammobox
        distribute_mags_and_bullets(self.database.session, self.gridItems)

    def writespawnabletypes(self):
        exportSpawnable(self.database.session, self.gridItems)

    def func2assign_raritiy(self):
        items = self.database.session.query(
            Item).filter(Item.nominal > 0).all()
        assign_rarity(items, self.database.session)

    def derivetypessubtypes(self):
        if self.database.get_mapselectValue(1).mapselectvalue == "Namalsk":
            # print("DEBUG derivetypessubtypes we are in a Namalsk map :", )
            for Item in self.gridItems:
                try:
                    for item_type, subtypes in categoriesNamalskDict.get(Item.cat_type).items():
                        for subtype, substrings in subtypes.items():
                            for item_substring in substrings:
                                if item_substring in Item.name.lower() and item_substring != "":
                                    Item.item_type = item_type
                                    Item.sub_type = subtype
                    if Item.cat_type in {"rifles", "pistols"}:
                        Item.cat_type = "weapons"
                except:
                    print("DEBUG item category not found :",
                          Item.cat_type, Item.name)
        else:
            for Item in self.gridItems:
                try:
                    for item_type, subtypes in categoriesDict.get(Item.cat_type).items():
                        for subtype, substrings in subtypes.items():
                            for item_substring in substrings:
                                if item_substring in Item.name.lower() and item_substring != "":
                                    Item.item_type = item_type
                                    Item.sub_type = subtype
                except:
                    print("DEBUG item category not found :",
                          Item.cat_type, Item.name)
        self.database.session.commit()

    def __CatFilter__(self, selection):
        if selection != "all":
            self.type_for_filter.set("all")
            self.sub_type_for_filter.set("all")

    def __TypeFilter__(self, selection):
        if selection != "all":
            self.cat_type_for_filter.set("all")
            self.sub_type_for_filter.set("all")

    def __SubTypeFilter__(self, selection):
        if selection != "all":
            self.cat_type_for_filter.set("all")
            self.type_for_filter.set("all")

    def __selectmodsfunction___(self):
        values = [(mod, var.get()) for mod, var in self.moddict.items()]
        self.moddlist = values
        self.selected_mods = [x[0] for x in self.moddlist if x[1] == 1]
        items = self.database.session.query(Item).filter(
            Item.mod.in_(self.selected_mods))
        self.gridItems = items
        self.__populate_items(self.gridItems)
        self.__create_nominal_info()
        self.type_for_filter.set("all")
        self.sub_type_for_filter.set("all")
        self.cat_type_for_filter.set("all")


# Updated to loop through selected items in the grid.

    def __update_item(self):
        def __update_helper(item, field, default_value):
            value_from_update_form = getattr(self, field).get()
            if value_from_update_form != default_value:
                # print("__update_item  :", value_from_update_form, default_value)
                setattr(item, field, value_from_update_form)

        for items in self.treeView.selection():
            item = self.treeView.item(items)
            id_of_interest = item["text"]
            item_to_update = self.database.session.query(
                Item).get(id_of_interest)
            __update_helper(item_to_update, "nominal", -1)
            __update_helper(item_to_update, "min", -1)
            __update_helper(item_to_update, "qmin", -1)
            __update_helper(item_to_update, "qmax", -1)
            __update_helper(item_to_update, "restock", -1)
            __update_helper(item_to_update, "lifetime", -1)
            __update_helper(item_to_update, "rarity", "")
            __update_helper(item_to_update, "cat_type", "")
            __update_helper(item_to_update, "item_type", "")
            __update_helper(item_to_update, "sub_type", "")
            __update_helper(item_to_update, "mod", "")
            __update_helper(item_to_update, "trader", "")
            __update_helper(item_to_update, "dynamic_event", -1)
            __update_helper(item_to_update, "count_in_hoarder", -1)
            __update_helper(item_to_update, "count_in_cargo", -1)
            __update_helper(item_to_update, "count_in_player", -1)
            __update_helper(item_to_update, "count_in_map", -1)

            usages = self.usagesListBox.curselection()
            usage_values = [self.usagesListBox.get(i) for i in usages]
            usages = ",".join(usage_values)
            if usages != "":
                setattr(item_to_update, "usage", usages)

            tiers = self.tiersListBox.curselection()
            tier_values = [self.tiersListBox.get(i) for i in tiers]
            tiers = ",".join(tier_values)
            if tiers != "":
                setattr(item_to_update, "tier", tiers)
            self.database.session.commit()
        self.__populate_items(self.gridItems)

    def __delete_item(self):
        for items in self.treeView.selection():
            item = self.treeView.item(items)
            itemid = item["text"]
            self.database.delete_item(itemid)
        self.__populate_items(self.gridItems)

    def __initiate_items(self, items=None):
        items = self.database.session.query(Item).filter(
            Item.mod.in_(self.selected_mods))
        self.gridItems = items
        self.__populate_items(items.all())

    def __populate_items(self, items):
        if self.tree.get_children() != ():
            self.tree.delete(*self.tree.get_children())

        for idx, i in enumerate(items):
            if idx % 2 == 0:
                self.tree.insert("", "end", text=i.id, value=[i.name, i.nominal, i.min, i.qmin, i.qmax,
                                                              i.restock, i.lifetime, i.usage, i.tier, i.rarity, i.cat_type, i.item_type, i.sub_type,
                                                              i.mod, i.trader, i.dynamic_event, i.count_in_hoarder, i.count_in_cargo,
                                                              i.count_in_player, i.count_in_map], tags=('evenrow',))
            else:
                self.tree.insert("", "end", text=i.id, value=[i.name, i.nominal, i.min, i.qmin, i.qmax,
                                                              i.restock, i.lifetime, i.usage, i.tier, i.rarity, i.cat_type, i.item_type, i.sub_type,
                                                              i.mod, i.trader, i.dynamic_event, i.count_in_hoarder, i.count_in_cargo,
                                                              i.count_in_player, i.count_in_map], tags=('oddrow',))
        self.tree.tag_configure('oddrow', background='#FFFFFF')
        self.tree.tag_configure('evenrow', background='#F5F5F5')

    def __search_like_name(self):
        searchname = str(self.searchName.get()).lower()
        if searchname != "":
            print(searchname)
            items = self.database.search_like_name(searchname)
            self.__populate_items(items)
            self.gridItems = items

    def __filter_usage_items(self):
        usagelst = []
        for i in self.LB_usage_filter.curselection():
            usagelst.append(self.LB_usage_filter.get(i))
            return usagelst

    def __filter_items(self):
        item_type = self.type_for_filter.get()
        sub_type = self.sub_type_for_filter.get()
        cat_type = self.cat_type_for_filter.get()
        self.LB_usage_filter.get(0)

        self.__filter_usage_items()

        if item_type != "all":
            items = self.database.filterby_type(
                self.selected_mods, 'item_type', item_type)
        elif sub_type != "all":
            items = self.database.filterby_type(
                self.selected_mods, 'sub_type', sub_type)
        elif cat_type != "all":
            items = self.database.filterby_type(
                self.selected_mods, 'cat_type', cat_type)
        else:
            items = self.database.session.query(Item).filter(
                Item.mod.in_(self.selected_mods)).filter(or_(*[Item.usage.contains(p) for p in self.__filter_usage_items()]))
        self.gridItems = items
        self.__create_nominal_info()
        self.__populate_items(items.all())

    def __fill_entry_frame(self, event):
        tree_row = self.tree.item(self.tree.focus())
        id = tree_row["text"]
        item = self.database.get_item(id)
        if item:
            self.id.set(id)
            self.name.set(item.name)
            self.nominal.set(-1)
            self.min.set(-1)
            self.qmin.set(-1)
            self.qmax.set(-1)
            self.lifetime.set(-1)
            self.restock.set(-1)
            self.mod.set("")
            self.trader.set("")
            usages = tree_row['values'][7]
            if usages != "":
                for i in range(len(usages)):
                    self.usagesListBox.select_clear(i)
            tiers = tree_row['values'][8]
            if tiers != "":
                for i in range(len(tiers)):
                    self.tiersListBox.select_clear(i)
            self.rarity.set("")
            self.cat_type.set("")
            self.item_type.set("")
            self.sub_type.set("")
            self.dynamic_event.set(-1)
            self.count_in_hoarder.set(-1)
            self.count_in_cargo.set(-1)
            self.count_in_map.set(-1)
            self.count_in_player.set(-1)

    def __create_nominal_info(self):
        self.infoFrame = Frame(self.window)
        self.infoFrame.grid(row=1, column=1, sticky="s,w,e")
        Label(self.infoFrame, text="Nominal counts: ").grid(
            row=0, column=0)
        self.totalNumDisplayed.set(self.database.getNominal(self.gridItems)[0])
        try:
            value = self.database.getNominalByCat(
                self.gridItems, "weapons")[0][1]
        except:
            value = 0
        self.totalWeaponDisplayed.set(value)
        Label(self.infoFrame, text="Displayed:").grid(row=0, column=1)
        Label(self.infoFrame, textvariable=self.totalNumDisplayed).grid(
            row=0, column=2)
        i = 3
        self.weaponNomTypes = {"ranged": 0, "ammo": 0,
                               "optic": 0, "mag": 0, "attachment": 0}
        for item_type in list(self.weaponNomTypes):
            var = StringVar()
            nomvar = (self.database.getNominalByType(
                self.gridItems, item_type))
            self.weaponNomTypes.update(nomvar)
            var.set(self.weaponNomTypes.get(item_type))
            self.nomVars.append(var)
            Label(self.infoFrame, text=item_type.capitalize() +
                  ":").grid(row=0, column=i)
            Label(self.infoFrame, textvariable=var).grid(row=0, column=i + 1)
            i += 4

    def __open_db_window(self):
        DB(self.window)
        self.initializeapp()

    def __import_link_window(self):
        LinkItem(self.window)
        self.initializeapp()

    def remove_menu(self):
        self.emptyMenu = Menu(self.window)
        self.window.config(menu=self.emptyMenu)

    def __open_items_window(self):
        NewItems(self.window)
        items = self.database.session.query(Item).filter(
            Item.mod.in_(self.selected_mods))
        self.gridItems = items
        self.__populate_items(items.all())
        self.updateAllMods(self.mods_menu)
        # self.__create_menu_bar()

    def __export_xml(self, mapname):
        file = filedialog.asksaveasfile(mode="a", defaultextension=".xml")
        if file != "":
            # mapname = self.database.get_mapselectValue(1).mapselectvalue
            xml_writer = XMLWriter(filename=file.name)
            items = self.database.session.query(Item).filter(
                Item.mod.in_(self.selected_mods))
            xml_writer.export_xml(items, mapname)

    def tree_view_sort_column(self, tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        try:
            l.sort(key=lambda t: int(t[0]), reverse=reverse)
        except ValueError:
            l.sort(reverse=reverse)
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)
        tv.heading(col, command=lambda: self.tree_view_sort_column(
            tv, col, not reverse))

    def __distribute_nominal(self):
        distribute_nominal(
            self.database,
            self.gridItems.filter(Item.nominal > 0),
            self.totalNumDisplayed.get(),
            self.distributorValue.get()
        )
        self.__populate_items(self.gridItems)

    def openTraderEditor(self):
        TraderEditor(self.window, self.selected_mods)

    def deriveammobox(self):
        init_database(self.config.get_database())
        items = self.database.search_like_name("ammobox")
        for item in items:
            exists = self.database.session.query(
                Ammobox).filter_by(name=item.name).first()
            if not exists:
                x = 0
                if "rnd" in item.name.lower():
                    x = item.name.lower().split("rnd")[-2].split("_")[-1]
                    x = re.sub("[^0-9]", "", x)
                item_obj = Ammobox(name=item.name, attachcount=int(x))
                self.database.session.add(item_obj)
        self.database.session.commit()


window = Tk()
GUI(window)
window.mainloop()
