import re
from database import Dao
from config import ConfigManager


def read_trader_file(file_path):

    with open(file_path, "r") as file:
        lines = file.readlines()

    traders = {}
    current_trader = None
    current_category = None

    for line in lines:
        line = line.strip()
        line = line.split("//", 1)[0].strip()  # Remove comments and extra whitespace
        line = re.sub(r"\t", "", line)
        if line is "":
            continue
        if line.startswith("<Trader>"):
            trader_str = line.replace("<Trader>", "")
            current_trader = trader_str.strip()
            traders[current_trader] = {}
        elif line.startswith("<Category>"):
            category_str = line.replace("<Category>", "")
            current_category = category_str.strip()
            traders[current_trader][current_category] = []
        elif current_trader is not None and current_category is not None:
            if line != "<FileEnd>":
                line_split = line.split(",")
                class_str = line_split[0]
                quant_str = line_split[1]
                buyprice_str = line_split[2]
                sellprice_str = line_split[3]
                item_data = {
                    "class": class_str.strip(),
                    "quantity": quant_str.strip(),
                    "buy_price": int(buyprice_str.strip()),
                    "sell_price": int(sellprice_str.strip()),
                }
                traders[current_trader][current_category].append(item_data)
    print(traders)
    return traders


def updateDrJonesdb(db, traders):
    for key in traders:
        print(key)
        for category, items in traders[key].items():
            for item in items:
                print(
                    category,
                    item["class"],
                    item["quantity"],
                    item["buy_price"],
                    item["sell_price"],
                )
                db.setDrJonesImportTrader(
                    key, category, item["buy_price"], item["sell_price"], item["class"]
                )
    tradernames = db.get_all_traders()
    config_manager = ConfigManager("config.xml")
    config_manager.set_traders(tradernames)
