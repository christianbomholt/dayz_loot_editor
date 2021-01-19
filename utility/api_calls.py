import requests

base_url = "http://ec2-18-195-220-162.eu-central-1.compute.amazonaws.com:5000"
endpoint = "/item_info/list"

def getweapons():
    weapons = requests.get(f'{base_url}{endpoint}')
    print(weapons.json())

    item_endpoint = "/item_info/"
    for weapon in weapons.json():
        weapon_info = requests.get(f'{base_url}{item_endpoint}{weapon}')
        print(weapon_info.json())

"""
def postweapons(Items):
    item = {
        "name ": item_name,
        "rarity" : rarity,
        "item_type": item_type,
        "sub_type": sub_type
    }
    for i in Items:
        item."""
         