column_definition = [
<<<<<<< HEAD
    {"text": "Name", "width": 250, "col_id": "#1", "stretch": "YES" },
    {"text": "Nominal", "width": 60, "col_id": "#2", "stretch": "YES" },
    {"text": "Min", "width": 50, "col_id": "#3", "stretch": "NO" },
    {"text": "Restock", "width": 60, "col_id": "#4", "stretch": "YES" },
    {"text": "Lifetime", "width": 60, "col_id": "#5", "stretch": "YES" },
    {"text": "Usage", "width": 200, "col_id": "#6", "stretch": "YES" },
    {"text": "Tier", "width": 200, "col_id": "#7", "stretch": "YES" },
    {"text": "Rarity", "width": 60, "col_id": "#8", "stretch": "YES" },
    {"text": "Category", "width": 60, "col_id": "#9", "stretch": "YES" },
    {"text": "Type", "width": 60, "col_id": "#10", "stretch": "YES" },
    {"text": "Sub Type", "width": 60, "col_id": "#11", "stretch": "YES" },
    {"text": "Mod", "width": 60, "col_id": "#12", "stretch": "YES" },
    {"text": "Trader", "width": 60, "col_id": "#13", "stretch": "YES" },
    {"text": "D", "width": 20, "col_id": "#14", "stretch": "NO" },
    {"text": "H", "width": 20, "col_id": "#15", "stretch": "NO" },
    {"text": "C", "width": 20, "col_id": "#16", "stretch": "NO" },
    {"text": "P", "width": 20, "col_id": "#17", "stretch": "NO" },
    {"text": "M", "width": 20, "col_id": "#18", "stretch": "NO" }
=======
    {
    "text": "Name",
    "width": 250,
    "col_id": "#1",
    "stretch": "YES"
    },
    {
    "text": "Name",
    "width": 250,
    "col_id": "#1",
    "stretch": "YES"
    },
    {
    "text": "Name",
    "width": 250,
    "col_id": "#1",
    "stretch": "YES"
    },
>>>>>>> ab096dd803e8b554d771a7cddb32e19eb6284ab0
]

gunSubTypesDict = {
    "Sidearms": [],
    "pistols": [],
    "rifles": [],
    "shotguns": [],
    "submachine guns": [],
    "assault rifles": [],
    "light machine guns": [],
    "sniper rifles": [],
    "anti material rifles": []
}

clothingSubTypesDict = {
    
    "eyewear":{ "glases": ["glasses"],
                "nightvision": ["nvg"],
                "melee": ["bat"]
                },
    "masks":{ "masks": ["mask"],
                "gas masks": ["gas"],
                "fun": ["Santa Beard"]
                },
    "gloves":{ "gloves": ["gloves"]
                },

    "headwear": ["hat"],
    "footwear": ["cap"],
    "pants": ["bandana"],
    "shirts": ["helm"],
    "vests": ["mask"],

    "Balaclava": ["balaclava"],
    "Shirts": ["shirt", "blouse"],
    "Hoodies": ["hoodie"],
    "Sweaters": ["sweater"],
    "Vests": ["vest"],
    "Jackets": ["jacket"],
    "Coats": ["coat"],
    "Suits": ["suit"],
    "Skirts Dresses": ["skirt", "dress_"],
    "Pants": ["pants", "breeches", "jeans"],
    "Shoes Boots": ["shoes", "sneakers", "boots", "wellies"],
    "Ghillie": ["ghillie"],
    "Holsters": ["holster"],
    "Pouches": ["pouch"],
    "Bags": ["bag"],
    "Handmade": []
}

foodSubTypesDict = {
    "Vegetables": ["mushroom", "apple", "pear", "plum", "pumpkin"],
    "Packaged Food": ["can", "cereal", "powdered"],
    "Meat": ["meat", "lard"],
    "Drinks": ["sodacan", "bottle", "canteen"],
    "Medical Supplies": ["saline", "bandage", "firstaid", "kitiv", "bloodTe", "Thermom"],
    "Medications": ["charcoal", "disinf", "vitamin", "tetracy", "painkil", "epine", "morph"],
    "Money Exchange": []
}

miscSubTypesDict = {
    "Tools (small)": ["screwdr", "wren", "sewingk", "pliers", "whetst", "saw", "cleaning", "chenkn", "anopen", "compas",
                      "hatche", "machet", "lockpick", "binoc"],
    "Tools (big)": ["lugwr", "crowb", "shov", "picka", "sledge", "woodAx", "ghterax"],
    "Electronics": ["battery", "onalrad", "megaph", "cableree", "electronicrep"],
    "Fire Lights": ["chemlight", "flare", "flashlight", "ablegas", "torch", "spotlight", "matchbox"],
    "Cooking Hunting Supplies": ["pot", "purific", "tripo", "beartra"],
    "Hardware Supplies": ["barrel", "canister", "handcuff", "netting", "seachest"],
    "Tents": ["tent"],
    "Seeds Lime": ["seeds"],
    "Melee": ["cattleprod", "BrassKnuckles", "NailedBaseba", "stunbat"]
}

# weaponSubTypesDict = {
#     "ranged": gunSubTypesDict,
#     "melee":{"knife": ["knife"],
#             "axe": ["axe"],
#             "melee": ["bat"]
#             },
#     "ammo": {"ammunition": ["ammo"]},
#     "optic": {"scopes": ["optic", "LRS", "scope"]},
#     "mag": {"magazines": ["mag"]},
#     "attachment": {"attachments": [""],
#                    "handguards": ["hndgrd", "handguard"],
#                    "bayonets": ["bayonet"],
#                    "buttstocks": ["bttstck", "buttstock"]}



weaponSubTypesDict = {
"bttstck": {"sub_type": "buttstocks", "item_type": "attatchment"},

}







vehicleSubTypesDict = {
    "Vehicle": ["OffroadHatchback", "CivilianSedan", "chassis"],
    "Vehicle Parts": {}
}

categoriesDict = {"weapons": weaponSubTypesDict,
                  "containers": clothingSubTypesDict,
                  "clothes": clothingSubTypesDict,
                  "food": foodSubTypesDict,
                  "tools": miscSubTypesDict,
                  "vehicles": vehicleSubTypesDict,
                  "vehiclesparts": {}}

weaponSubTypes = list(weaponSubTypesDict.keys())
categories = list(categoriesDict.keys())

usages = ["Military",
          "Prison",
          "School",
          "Coast",
          "Village",
          "Industrial",
          "Medic",
          "Police",
          "Hunting",
          "Town",
          "Farm",
          "Firefighter",
          "Office"]

usagesAbr = ["Mil.",
             "Pris.",
             "School",
             "Coast",
             "Vil.",
             "Ind.",
             "Med.",
             "Pol.",
             "Hunt.",
             "Town",
             "Farm",
             "Firef.",
             "Office"]

tiers = ["Tier1", "Tier2", "Tier3", "Tier4"]

tags = ["shelves", "floor"]

flags = ["count_in_cargo",
         "count_in_hoarder",
         "count_in_map",
         "count_in_player",
         "crafted",
         "deloot"]

weaponTraderCat = [word.lower() for word in gunSubTypesDict.keys()]
weaponTraderCat.append("gun")
weaponTraderCat.append("melee")

allcats = []


def appendKeys(dict, tolist):
    for cat in dict.keys():
        tolist.append(cat)
    return tolist


allcats = appendKeys(gunSubTypesDict, allcats)
allcats = appendKeys(clothingSubTypesDict, allcats)
allcats = appendKeys(foodSubTypesDict, allcats)
allcats = appendKeys(miscSubTypesDict, allcats)
allcats = appendKeys(vehicleSubTypesDict, allcats)


def traderCatSwitcher(argument):
    
    argument = argument.lower()

    if "magazine" in argument or "barrel_" in argument:
        return "M"

    elif argument == "vehicle":
        return "V"

    elif argument in weaponTraderCat:
        return "W"

    elif "steakmeat" in argument:
        return "S"

    return "*"
