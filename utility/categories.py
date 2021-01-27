column_definition = [
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
    "eyewear":{ "glasses": ["glasses","goggles"],
                "nightvision": ["nvg"],
                "melee": ["bat"]
                },
    "headwear":{    "masks": ["mask"],
                    "hat": ["hat","cap","beret"],
                    "helmet": ["helm"],
                    "balaclava": ["balaclava"],
                    "bandana": ["bandana"],
                    "gas masks": ["gas"],
                    "fun": ["santasbeard"]
                },
    "gloves":{      "gloves": ["gloves"]
                },
    "footwear":{    "shoes": ["shoes","sneakers"],
                    "boots": ["boot", "wellies"],
                },
    "lowerbody":{   "pants": ["pant", "breech", "jeans"],
                    "skirt/dress": ["skirt", "dress_"]
                },
    "upperbody":{   "vests": ["vest"],
                    "shirts": ["shirt", "blouse"],
                    "hoodies": ["hoodie"],
                    "sweaters": ["sweater"],
                    "vests": ["vest"],
                    "jackets": ["jacket"],
                    "coats": ["coat"],
                    "suits": ["suit"]
                },
    "ghillie":{   "ghillie": ["ghillie"]
                },
    "accessory":{   "belt": ["belt"],
                    "armband": ["armband"]
                }                
}

foodSubTypesDict = {
    "natural":  {   "vegetables": ["mushroom", "apple", "pear", "plum", "pumpkin","zucchini","rice","potato","pepper","tomato"],
                    "animal":["meat", "lard","steak"]
                },
    "man made": {   "packaged food": ["can", "cereal", "powdered","marmala"]
                },
    "drink":    {   "drink": ["sodacan", "bottle", "canteen","waterbottle"]   
                },
    "medical":  {   "firstaid": ["saline", "bandage", "firstaid", "kitiv", "bloodte", "thermom"],
                    "medicin": ["charcoal", "disinf", "vitamin", "tetracy", "painkil", "epine", "morph"]
                }
}

containerSubTypesDict = {
    "bags":     {   "bags": ["bag"]
                },
    "l-storage":{   "tents": ["tent"],
                    "crate": ["crate"],
                    "barrel" :  ["barrel"]
                },
    "s-storage":{   "bear": ["bear"] ,
                    "giftbox": ["giftbox"],
                    "ammobox": ["ammobox"] 
                },
    "medical":  {   "firstaid": ["saline", "bandage", "firstaid", "kitiv", "bloodte", "thermom"],
                    "medicin": ["charcoal", "disinf", "vitamin", "tetracy", "painkil", "epine", "morph"]
                }
}


toolsSubTypesDict = {
    "s-tools":  {   "handtools": ["screwdr", "wren", "sewingk", "pliers", "whetst", "saw", "cleaning", "chenkn", "anopen", "compas",
                      "hatche", "machet", "lockpick", "binoc","hammer"],
                    "melee": ["cattleprod", "brassknuckles", "bat", "stunbat"],
                    "knife": ["knife"]
                },
    "l-tools":  {   "largetools": ["lugwr", "crowb", "shov", "picka", "sledge", "woodax", "ghterax","pipe"]
                },
    "electro":  {   "electro": ["battery", "radio", "megaph", "cableree", "electronicrep","xmaslights","rangef","baseradio"]
                },
    "lightsource":{ "light": ["chemlight", "flare", "flashlight", "ablegas", "torch", "spotlight"]
                },
    "cooking":  {   "cooking": ["pot", "purific", "tripo","fryingpan","firep","oven"]
                },
    "hardware": {   "hardware": ["barrel", "canister", "handcuff", "netting", "seachest","rope"]
                },
    "tents":    {   "person tent": ["tent"]
                },
    "fire":    {   "fire": ["firewood","lighter","bark","handdri", "matchbox","woodenstick"]
                },
    "farming":  {   "farming": ["seeds","plant","lime","antipestsspray","gardenplot"]
                },
    "hunt/fish":  { "hunt/fish": ["hook","rod","pelt","trap","gardenplot","bait","smallg","burlap","guts","bone"]
                },
    "personal":  {  "medical": ["bandage","blood","heatpack","rag","saline","tetracyclineantibiotics","thermo","vitaminbottle","epinephrine","morphine","painkillertablets","defibrillator","charcoaltablets"],
                    "equiptment": ["pen","paper"]
                },
    "bases":  {   "basestuff": ["flag","nail","shelter","barbedwire","fencekit","metalwire","woodenlog","woodenplank","watchtowerkit","pileofwoodenplanks"]
                },
    "automotive":  {   "automotive": ["sparkp","headligh","engineo","carradiator","tirerepairkit"]
                }                
}

pistolsNamalskSubTypesDict = {
    "pistols": {
        "Sidearms": [],
        "pistols": ["fnx45","deagle","makarov","glock","colt1911","engraved1911","cz75","mkii","magnum"]
            }
}

riflesNamalskSubTypesDict = {
    "rifles": {
        "rifles": [],
        "shotguns": ["shotgun","saiga"],
        "submachine guns": ["mp5k","ump45","cz61"],
        "assault rifles": ["ak101","ak74","m4a1","akm","aks74u","fal"],
        "light machine guns": [],
        "sniper rifles": ["mosin9130","svd","vss"],
        "hunting rifles": ["b95","cz527","Izh18","repeater","winchester70"],
        "semi-automatic rifles": ["ruger1022","sks"],
        "anti material rifles": []
            }
}

explosivesSubtypeDict = {
    "explosives": {
        "explosives": ["grenade","mine"]
            }
}

weaponSubTypesDict = {
    "ranged": {
        "Sidearms": [],
        "pistols": ["fnx45","deagle","makarov","glock","colt1911","engraved1911","cz75","mkii","magnum"],
        "rifles": [],
        "shotguns": ["shotgun","saiga"],
        "submachine guns": ["mp5k","ump45","cz61"],
        "assault rifles": ["ak101","ak74","m4a1","akm","aks74u","fal"],
        "light machine guns": [],
        "sniper rifles": ["mosin9130","svd","vss"],
        "hunting rifles": ["b95","cz527","Izh18","repeater","winchester70"],
        "semi-automatic rifles": ["ruger1022","sks"],
        "anti material rifles": []
            },
    "melee":{
        "knife": ["knife"],
        "axe": ["axe"],
        "melee": ["bat"]
            },
    "ammo": {
        "single ammo": ["ammo_"],
        "boxed ammo": ["ammob"],
        },
    "optic": {
        "scopes": ["optic", "lrs", "scope"]
        },
    "mag": {
        "magazines": ["mag"]
        },
    "explosive": {
        "explosive": ["grenade"]
        },
    "attachment": {
        "attachments": [""],
        "handguards": ["hndgrd", "handguard"],
        "bayonets": ["bayonet"],
        "suppressor": ["suppressor"],
        "compensator" : ["compensator"],
        "light" : ["universallight","tlrlight"],
        "buttstocks": ["bttstck", "buttstock"]}
}

vehicleSubTypesDict = {
    "vehicle":  {
        "car": ["hatchback","sedan"],
        "truck": ["truck"]}
}

vehiclepartsSubTypesDict = {
    "vehicleparts":  {
        "door": ["door"],
        "trunk": ["trunk"],
        "hood": ["hood"],
        "wheel": ["wheel"]}
}

categoriesDict = {"weapons": weaponSubTypesDict,
                  "containers": containerSubTypesDict,
                  "clothes": clothingSubTypesDict,
                  "food": foodSubTypesDict,
                  "tools": toolsSubTypesDict,
                  "vehicles": vehicleSubTypesDict,
                  "vehiclesparts": vehiclepartsSubTypesDict,
                  "object":{}}

categoriesNamalskDict = {
                  "pistols": pistolsNamalskSubTypesDict,
                  "rifles": riflesNamalskSubTypesDict,
                  "weapons": weaponSubTypesDict,
                  "explosives" : explosivesSubtypeDict,
                  "containers": containerSubTypesDict,
                  "clothes": clothingSubTypesDict,
                  "food": foodSubTypesDict,
                  "tools": toolsSubTypesDict,
                  "vehicles": vehicleSubTypesDict,
                  "vehiclesparts": vehiclepartsSubTypesDict,
                  "object":{}}



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

allcats = appendKeys(weaponSubTypesDict, allcats)
allcats = appendKeys(clothingSubTypesDict, allcats)
allcats = appendKeys(foodSubTypesDict, allcats)
allcats = appendKeys(toolsSubTypesDict, allcats)
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
