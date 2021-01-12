gunSubTypesDict = {
    "Sidearms": [],
    "Pistols": [],
    "Rifles": [],
    "Shotguns": [],
    "Submachine Guns": [],
    "Assault Rifles": [],
    "Light Machine Guns": [],
    "Sniper Rifles": [],
    "Anti Material Rifles": []
}

clothingSubTypesDict = {
    "Glasses": ["glasses", "goggles"],
    "Armbands": ["armband"],
    "Gloves": ["gloves"],
    "Hats": ["hat"],
    "Caps": ["cap"],
    "Bandanas": ["bandana"],
    "Helmets": ["helm"],
    "Masks": ["mask"],
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

weaponSubTypesDict = {
    "gun": gunSubTypesDict,
    "ammo": {"Ammunition": ["ammo"]},
    "optic": {"Scopes": ["optic", "LRS", "scope"]},
    "mag": {"magazines": ["mag"]},
    "attachment": {"Attachments": [""],
                   "Handguards": ["hndgrd", "handguard"],
                   "Bayonets": ["bayonet"],
                   "Buttstocks": ["bttstck", "buttstock"]}
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
