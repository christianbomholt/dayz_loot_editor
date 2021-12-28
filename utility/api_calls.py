import requests
from model import Item


class ApiCalls():
    pass


def apipush(session):
    # base_url = "http://ec2-18-195-220-162.eu-central-1.compute.amazonaws.com:5000"
    base_url = "http://localhost:8000"
    item_endpoint = "/items_update/"
    # items_to_change = session.query(Item).limit(5)
    items_to_push = session.query(Item).filter(Item.rarity != "undefined")
    print(items_to_push.all())

    for item in items_to_push:
        payload = {
            "name": item.name,
            "rarity": item.rarity,
            "item_type": item.item_type,
            "sub_type": item.sub_type
        }
        url = f'{base_url}{item_endpoint}'
        # r = requests.put(url, json=payload)


def apipull(session):
    # base_url = "http://ec2-18-195-220-162.eu-central-1.compute.amazonaws.com:5000"
    base_url = "http://localhost:8000"
    endpoint = "/item_list"
    weapons = requests.get(f'{base_url}{endpoint}')
    item_endpoint = "/item_info/"
    for weapon in weapons.json():
        weapon_info = requests.get(f'{base_url}{item_endpoint}{weapon}')
        print(weapon_info.json())
        weapon_json = weapon_info.json()
        exists = session.query(Item).filter(
            Item.name == weapon_json.get("name")).first()
        if exists:
            print(exists.rarity, "->", weapon_json.get("rarity"))
            exists.rarity = weapon_json.get("rarity")
            exists.item_type = weapon_json.get("item_type")
            exists.sub_type = weapon_json.get("sub_type")
            session.commit()
