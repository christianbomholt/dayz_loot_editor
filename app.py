from tkinter import Tk, Menu, IntVar, Frame, Label, StringVar, Entry, Listbox, END, OptionMenu, Checkbutton, Button
from tkinter import ttk, VERTICAL, HORIZONTAL, LabelFrame
from config import ConfigManager
from database.dao import Dao
from model.item import Item
from ui.db import DB
from ui.new_items import NewItems
from ui.setprices import TraderEditor
from utility.combo_box_manager import ComboBoxManager
from utility.distibutor import Dist
from config.ini_manager import INIManager
from xml_manager.xml_writer import XMLWriter
import tkinter.filedialog as filedialog


class GUI(object):
    def __init__(self, main_container: Tk):
        #
        self.config = ConfigManager("config.xml")
        self.ini_manger = INIManager("app.ini")
        self.database = Dao(self.ini_manger.read_ini("Database", "Database_Name"))
        self.selectedMods = ['Vanilla','Mod 1']
        #
        self.window = main_container
        self.window.wm_title("Loot Editor v0.98.7")
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=3)
        self.menu_bar = Menu(self.window)
        #
        self.__create_menu_bar()
        self.__create_entry_frame()
        self.__create_tree_view()
        self.__create_side_bar()
        self.__populate_items()
        #
        self.tree.bind("<ButtonRelease-1>", self.__fill_entry_frame)

    def __create_menu_bar(self):
        # file menus builder
        file_menu = Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Setup Database", command=self.__open_db_window)
        file_menu.add_separator()
        file_menu.add_command(label="Add Items", command=self.__open_items_window)
        file_menu.add_command(label="Export XML File", command=self.__export_xml)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.window.destroy)

        # database menus builder

        # mod menus builder
        mods_menu = Menu(self.menu_bar, tearoff=0)
        mods_menu.add_command(label="Deselect All")
        mods_menu.add_command(label="Select All")
        mods_menu.add_separator()
        for mod in self.config.get_mods():
            int_var = IntVar()

            mods_menu.add_checkbutton(label=mod, variable=int_var)
            int_var.set(1)

        # help menus builder
        help_menu = Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="You are totally on your own")

        # building menu bar
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        self.menu_bar.add_cascade(label="Mods In Use", menu=mods_menu)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

        # configuring menu bar
        self.window.config(menu=self.menu_bar)

    def __create_entry_frame(self):
        self.entryFrameHolder = Frame(self.window)
        self.entryFrameHolder.grid(row=0, column=0, sticky="nw")
        self.entryFrame = Frame(self.entryFrameHolder)
        self.entryFrame.grid(padx=8, pady=6)
        # labels
        Label(self.entryFrame, text="Name").grid(row=0, column=0, sticky="w", pady=5)
        Label(self.entryFrame, text="Nominal").grid(row=1, column=0, sticky="w", pady=5)
        Label(self.entryFrame, text="Min").grid(row=2, column=0, sticky="w", pady=5)
        Label(self.entryFrame, text="Restock").grid(row=3, column=0, sticky="w", pady=5)
        Label(self.entryFrame, text="Lifetime").grid(row=4, column=0, sticky="w", pady=5)
        Label(self.entryFrame, text="Usages").grid(row=5, column=0, sticky="w", pady=5)
        Label(self.entryFrame, text="Tiers").grid(row=6, column=0, sticky="w", pady=5)
        Label(self.entryFrame, text="Category").grid(row=7, column=0, sticky="w", pady=5)
        Label(self.entryFrame, text="Type").grid(row=8, column=0, sticky="w", pady=5)
        Label(self.entryFrame, text="Sub Type").grid(row=9, column=0, sticky="w", pady=5)
        Label(self.entryFrame, text="Rarity").grid(row=10, column=0, sticky="w", pady=5)
        Label(self.entryFrame, text="Mod").grid(row=11, column=0, sticky="w", pady=5)
        Label(self.entryFrame, text="Trader").grid(row=12, column=0, sticky="w", pady=5)
        # input variables
        self.id = IntVar()
        self.name = StringVar()
        self.nominal = IntVar()
        self.min = IntVar()
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
        self.count_in_map = IntVar()
        self.count_in_player = IntVar()
        # form fields
        self.nameField = Entry(self.entryFrame, textvariable=self.name)
        self.nameField.grid(row=0, column=1, sticky="w")
        self.nominalField = Entry(self.entryFrame, textvariable=self.nominal)
        self.nominalField.grid(row=1, column=1, sticky="w")
        self.minField = Entry(self.entryFrame, textvariable=self.min)
        self.minField.grid(row=2, column=1, sticky="w")
        self.restockField = Entry(self.entryFrame, textvariable=self.restock)
        self.restockField.grid(row=3, column=1, sticky="w")
        self.lifetimeField = Entry(self.entryFrame, textvariable=self.lifetime)
        self.lifetimeField.grid(row=4, column=1, sticky="w")
        self.usagesListBox = Listbox(
            self.entryFrame,
            height=4,
            selectmode="multiple",
            exportselection=False,
        )
        self.usagesListBox.grid(row=5, column=1, pady=5, sticky="w")
        usages = self.config.get_usages()
        for i in usages:
            self.usagesListBox.insert(END, i)

        self.tiersListBox = Listbox(
            self.entryFrame,
            height=4,
            selectmode="multiple",
            exportselection=False,
        )
        self.tiersListBox.grid(row=6, column=1, pady=5, sticky="w")
        tiers = self.config.get_tiers()
        for i in tiers:
            self.tiersListBox.insert(END, i)
        self.cat_typeOption = OptionMenu(
            self.entryFrame, self.cat_type, *self.config.get_cat_types()[1:]
        )
        self.cat_typeOption.grid(row=7, column=1, sticky="w", pady=5)
        self.typeOption = OptionMenu(
            self.entryFrame, self.item_type, *self.config.get_types()[1:]
        )
        self.typeOption.grid(row=8, column=1, sticky="w", pady=5)
        self.subtypeAutoComp = ComboBoxManager(
            self.entryFrame, self.config.get_sub_types(), highlightthickness=1
        )
        self.subtypeAutoComp.grid(row=9, column=1, sticky="w", pady=5)
        self.rarityOption = OptionMenu(
            self.entryFrame, self.rarity, *self.config.get_rarities()
        )
        self.rarityOption.grid(row=10, column=1, sticky="w", pady=5)
        self.modField = Entry(self.entryFrame, textvariable=self.mod)
        self.modField.grid(row=11, column=1, sticky="w", pady=5)
        self.traderField = Entry(self.entryFrame, textvariable=self.trader)
        self.traderField.grid(row=12, column=1, sticky="w")
        # check boxes frame
        self.checkBoxFrame = Frame(self.entryFrameHolder)
        self.checkBoxFrame.grid(row=1, column=0, columnspan=2, sticky="w")
        self.dynamic_event_check = Checkbutton( 
            self.checkBoxFrame, text="Dynamic Event", variable=self.dynamic_event, onvalue = 1, offvalue = 0
        )
        self.dynamic_event_check.grid(row=0, column=0, sticky="w")
        self.count_in_cargo_check = Checkbutton(
            self.checkBoxFrame, text="Count in Cargo", variable=self.count_in_cargo, onvalue = 1, offvalue = 0
        )
        self.count_in_cargo_check.grid(row=1, column=0, sticky="w")
        self.count_in_hoarder_check = Checkbutton(
            self.checkBoxFrame, text="Count in Hoarder", variable=self.count_in_hoarder, onvalue = 1, offvalue = 0
        )
        self.count_in_hoarder_check.grid(row=2, column=0, sticky="w")
        self.count_in_map_check = Checkbutton(
            self.checkBoxFrame, text="Count in Map", variable=self.count_in_map, onvalue = 1, offvalue = 0
        )
        self.count_in_map_check.grid(row=3, column=0, sticky="w")
        self.count_in_player_check = Checkbutton( 
            self.checkBoxFrame, text="Count in Player", variable=self.count_in_player, onvalue = 1, offvalue = 0
        )
        self.count_in_player_check.grid(row=4, column=0, sticky="w")

        Button(
            self.checkBoxFrame, text="Update", width=8, command=self.__update_item
        ).grid(row=5, column=0, pady=5, sticky="w")

        Button(
            self.checkBoxFrame, text="Delete", width=8, command=self.__delete_item
        ).grid(row=5, column=1, pady=5, sticky="w")

    def __create_tree_view(self):
        self.treeFrame = Frame(self.window)
        self.treeFrame.grid(row=0, column=1, sticky="nsew")
        self.treeFrame.grid_rowconfigure(0, weight=1)
        self.treeFrame.grid_columnconfigure(1, weight=1)
        self.column_info = self.config.get_tree_heading()
        self.tree = ttk.Treeview(self.treeFrame, columns=self.column_info[0], height=40)
        for col in self.column_info[1]:
            self.tree.heading(
                col[2],
                text=col[0],
                command=lambda _col=col[0]: self.tree_view_sort_column(
                    self.tree, _col, False
                ),
            )
            self.tree.column(col[2], width=col[1], stretch=col[3])

        self.tree.grid(row=0, column=0, sticky="nsew")
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

        self.filterFrame = LabelFrame(self.filterFrameHolder, text="Filter")
        self.filterFrame.grid(row=1, column=0, pady=5)

        Label(self.filterFrame, text="Type").grid(row=1, column=0, sticky="w")
        Label(self.filterFrame, text="Subtype").grid(row=2, column=0, sticky="w")

        self.type_for_filter = StringVar()
        self.type_for_filter.set("all")
        OptionMenu(
            self.filterFrame, self.type_for_filter, *self.config.get_types()
        ).grid(row=1, column=1, sticky="w", padx=5)
        self.sub_type_combo_for_filter = ComboBoxManager(
            self.filterFrame,
            self.config.get_sub_types(),
            highlightthickness=1,
            width=15,
        )
        self.sub_type_combo_for_filter.grid(row=2, column=1, sticky="w", pady=5, padx=5)

        Button(
            self.filterFrame, text="Filter", width=12, command=self.__filter_items
        ).grid(columnspan=2, pady=5, padx=10, sticky="nesw")
        self.buttons_frame = Frame(self.filterFrame)
        self.buttons_frame.grid(row=4, columnspan=2)
        # Button(self.buttons, text="view linked items", width=12).grid(row=3)
        Button(
            self.buttons_frame,
            text="Search like Name",
            width=14,
            command=self.__search_like_name,
        ).grid(row=4)
#
# This is were we have the test button
#         
        Button(
            self.buttons_frame,
            text="Trader Editor",
            width=14,
            command=self.openTraderEditor,
        ).grid(row=5)

        Button(
            self.buttons_frame,
            text="Distributor",
            width=14,
            command=self.Distributor,
        ).grid(row=6)

# Updated to loop through selected items in the grid.
    def __update_item(self):
        for items in self.treeView.selection():
            item = self.treeView.item(items)
            print("DEBUG Item", item)
            updated_item = Item()
            updated_item.id = item["text"]
            updated_item.name = item[0]
            #nominal
            nominal = self.nominal.get()
            if nominal != -1:
                updated_item.nominal = nominal
            else:
                updated_item.nominal = item.nominal    
            #min
            min = self.min.get()
            if min != -1:
                updated_item.min = min
            else:
                updated_item.min = item.min    
            #lifetime
            lifetime = self.lifetime.get()
            if lifetime != -1:
                updated_item.lifetime = lifetime
            #restock
            restock = self.restock.get()
            if restock != -1:
                updated_item.restock = restock
            usages = self.usagesListBox.curselection()
            values = [self.usagesListBox.get(i) for i in usages]
            usages = ",".join(values)
            updated_item.usage = usages
            tiers = self.tiersListBox.curselection()
            tier_values = [self.tiersListBox.get(i) for i in tiers]
            tiers = ",".join(tier_values)
            updated_item.tier = tiers
            #rarity
            rarity = self.rarity.get()
            if rarity != '':
                updated_item.rarity = rarity
            #cat_type
            cat_type = self.cat_type.get()
            if cat_type != '':
                updated_item.cat_type = cat_type
            #item_type
            item_type = self.item_type.get()
            if item_type != '':
                updated_item.item_type = item_type
            #sub_type
#            restock = self.restock.get()
#            if restock != '':
#            updated_item.restock = restock
#            if (sub_type := self.subtypeAutoComp()) != '':
#                updated_item.sub_type = sub_type
            #mod
            mod = self.mod.get()
            if mod != '':
                updated_item.mod = mod
            #trader
            trader = self.trader.get()
            if trader != '':
                updated_item.trader = trader
            #dynamic_event
            dynamic_event = self.dynamic_event.get()
            if dynamic_event != -1:
                updated_item.dynamic_event = dynamic_event
            #count_in_hoarder
            count_in_hoarder = self.count_in_hoarder.get()
            if count_in_hoarder != -1:
                updated_item.count_in_hoarder = count_in_hoarder
            #count_in_cargo
            count_in_cargo = self.count_in_cargo.get()
            if count_in_cargo != -1:
                updated_item.count_in_cargo = count_in_cargo
            #count_in_map
            count_in_map = self.count_in_map.get()
            if count_in_map != -1:
                updated_item.count_in_map = count_in_map
            #count_in_player
            count_in_player = self.count_in_player.get()
            if count_in_player != -1:
                updated_item.count_in_player = count_in_player
            self.database.update_item(updated_item)
        self.__populate_items()

    def __delete_item(self):
        for items in self.treeView.selection():
            item = self.treeView.item(items)
            itemid = item["text"]
            self.database.delete_item(itemid)
        self.__populate_items()

    def __populate_items(self, items=None):
        if items is None:
            items = self.database.all_items()
        if self.tree.get_children() != ():
            self.tree.delete(*self.tree.get_children())
        for i in items:
            self.tree.insert("", "end", text=i[0], value=i[1:14])

    def __search_by_name(self):
        if self.name.get() != "":
            self.__populate_items(self.database.search_by_name(self.name.get()))

    def __search_like_name(self):
        if self.name.get() != "":
            self.__populate_items(self.database.search_like_name(self.name.get()))

    def __filter_items(self):
        item_type = self.type_for_filter.get()
        if item_type == "all":
            self.__populate_items(self.database.all_items())
        else:
            if self.sub_type_combo_for_filter.get() != "":
                sub_type = self.sub_type_combo_for_filter.get()
            else:
                sub_type = None
            self.__populate_items(self.database.filter_items(item_type, sub_type))    
          #  self.__populate_items(self.database.search_by_name(item_type, sub_type))

    def __fill_entry_frame(self, event):
        tree_row = self.tree.item(self.tree.focus())
        id = tree_row["text"]
        item = self.database.get_item(id)
        self.id.set(id)
        self.name.set(item.name)
        self.nominal.set(-1)
        self.min.set(-1)
        self.lifetime.set(-1)
        self.restock.set(-1)
        self.mod.set("")
        self.trader.set("")
        for i in range(len(usages)):
            self.usagesListBox.select_clear(i)
        for i in range(len(tiers)):
            self.tiersListBox.select_clear(i)
        self.rarity.set("")
        self.cat_type.set("")
        self.type.set("")
        self.subtypeAutoComp.set_value("")
        self.dynamic_event.set(-1)
        self.count_in_hoarder.set(-1)
        self.count_in_cargo.set(-1)
        self.count_in_map.set(-1)
        self.count_in_player.set(-1)

    """
    def __fill_entry_frame(self, event):
        tree_row = self.tree.item(self.tree.focus())
        id = tree_row["text"]
        item = self.database.get_item(id)
        self.id.set(id)
        self.name.set(item.name)
        self.nominal.set(item.nominal)
        self.min.set(item.min)
        self.lifetime.set(item.lifetime)
        self.restock.set(item.restock)
        self.mod.set(item.mod)
        self.trader.set(item.trader)
        usages = self.config.get_usages()
        _usages = str(item.usage).split(",")
        for i in range(len(usages)):
            self.usagesListBox.select_clear(i)
        for i in range(len(usages)):
            for j in _usages:
                if usages[i] == j:
                    self.usagesListBox.select_set(i)
        tiers = self.config.get_tiers()
        _tiers = str(item.tier).split(",")
        for i in range(len(tiers)):
            self.tiersListBox.select_clear(i)
        for i in range(len(tiers)):
            for j in _tiers:
                if tiers[i] == j:
                    self.tiersListBox.select_set(i)

        self.rarity.set(item.rarity)
        self.cat_type.set(item.cat_type)
        self.type.set(item.item_type)
        self.subtypeAutoComp.set_value(item.sub_type)
        self.dynamic_event.set(item.dynamic_event)
        self.count_in_hoarder.set(item.count_in_hoarder)
        self.count_in_cargo.set(item.count_in_cargo)
        self.count_in_map.set(item.count_in_map)
        self.count_in_player.set(item.count_in_player) """
    """
    def __create_nominal_info(self):
        self.infoFrame = Frame(self.window)
        self.infoFrame.grid(row=1, column=1, sticky="s,w,e")

        Label(self.infoFrame, text="overall nominal / delta:").grid(row=0, column=0)

        Label(self.infoFrame, text="Displayed:").grid(row=0, column=1)
        Label(self.infoFrame, textvariable=self.totalNomDisplayed).grid(row=0, column=2)
        i = 3

        for item_type in itemTypes:
            var = StringVar()
            delta_start = StringVar()

            self.start_nominal.append(Dao.getNominalByType(item_type))
            var.set(dao.getNominalByType(item_type))
            self.nomVars.append(var)
            delta_start.set(0)
            self.deltaNom.append(delta_start)

            Label(self.infoFrame, text=item_type.capitalize() + ":").grid(row=0, column=i)
            Label(self.infoFrame, textvariable=var).grid(row=0, column=i + 1)
            Label(self.infoFrame, text="/").grid(row=0, column=i + 2)
            Label(self.infoFrame, textvariable=delta_start).grid(row=0, column=i + 3)

            i += 4

    def __update_nominal_info(self):
        for i in range(len(self.nomVars)):
            nominal = dao.getNominalByType(itemTypes[i])
            self.nomVars[i].set(nominal)
            try:
                self.deltaNom[i].set(nominal - self.start_nominal[i])
            except TypeError:
                pass
                #self.deltaupdateNominalInfoNom[i].set(nominal) """

    def __open_db_window(self):
        DB(self.window)

    def __open_items_window(self):
        NewItems(self.window)
        self.__populate_items()

    def __export_xml(self):
        file = filedialog.asksaveasfile(mode="a", defaultextension=".xml")
        xml_writer = XMLWriter(filename=file.name)
        items = self.database.get_items()
        xml_writer.export_xml(items)

    def tree_view_sort_column(self, tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children("")]
        l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            tv.move(k, "", index)

        # reverse sort next time
        tv.heading(
            col,
            command=lambda _col=col: self.tree_view_sort_column(tv, _col, not reverse),
        )

    def Distributor(self,):
        items = self.database.get_items()
        Dist.distribute(items,1000,1000,1000,[1,1])    

    def openTraderEditor(self):
        TraderEditor(self.window,self.selectedMods)

"""     def OnChange(value, name, *pargs):
        self.update_dict[name] =  value.get()
        print(self.update_dict)
#        do more. set av value based on omv value
        self.nominal.trace_add("write", lambda *pargs: OnChange(self.nominal,"nominal",*pargs))
        self.min.trace_add("write", lambda *pargs: OnChange(self.min,"min",*pargs))
        self.restock.trace_add("write", lambda *pargs: OnChange(self.restock,"restock",*pargs))
        self.lifetime.trace_add("write", lambda *pargs: OnChange(self.lifetime,"lifetime",*pargs))  
        self.usage.trace_add("write", lambda *pargs: OnChange(self.usage,"usage",*pargs))
        self.tier.trace_add("write", lambda *pargs: OnChange(self.tier,"tier",*pargs))
        self.rarity.trace_add("write", lambda *pargs: OnChange(self.rarity,"rarity",*pargs))
        self.cat_type.trace_add("write", lambda *pargs: OnChange(self.cat_type,"cat_type",*pargs))        
        self.item_type.trace_add("write", lambda *pargs: OnChange(self.item_type,"item_type",*pargs))
        self.sub_type.trace_add("write", lambda *pargs: OnChange(self.sub_type,"sub_type",*pargs))
        self.mod.trace_add("write", lambda *pargs: OnChange(self.mod,"mod",*pargs))
        self.trader.trace_add("write", lambda *pargs: OnChange(self.trader,"trader",*pargs)) """

window = Tk()
GUI(window)
window.mainloop()
