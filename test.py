import re

filename = "TraderConfig.txt"

with open(filename, "r") as file:
    lines = file.readlines()

traders = {}
current_trader = None
current_category = None
current_item = None
current_quantity = None
current_buyprice = None
current_sellprice = None
for line in lines:
    line = line.strip()
    line = line.split("//", 1)[0].strip()  # Remove comments and extra whitespace
    line = re.sub(r"\t", "", line)
    if line == "":
        continue
    if line.startswith("<Trader>"):
        trader_str = line.replace("<Trader>", "")
        current_trader = trader_str
        traders[current_trader] = {}
    elif line.startswith("<Category>"):
        category_str = line.replace("<Category>", "")
        current_category = category_str
        traders[current_trader][current_category] = []
    elif current_trader is not None and current_category is not None:
        if line != "<FileEnd>":
            line_split = line.split(",")
            class_str = line_split[0]
            quant_str = line_split[1]
            buyprice_str = line_split[2]
            sellprice_str = line_split[3]
            item_data = {
                "class": class_str,
                "quantity": quant_str,
                "buy_price": int(buyprice_str),
                "sell_price": int(sellprice_str),
            }
            traders[current_trader][current_category].append(item_data)
print(traders)
