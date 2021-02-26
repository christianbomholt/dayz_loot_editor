import requests
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Item
Base = declarative_base()

engine = create_engine('sqlite:///../../Chernarus9.db')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()
# base_url = "http://ec2-18-195-220-162.eu-central-1.compute.amazonaws.com:5000"

base_url = "http://localhost:8000"

item_endpoint = "/items_update/"

items_to_change = session.query(Item).limit(5)

print(items_to_change.all())

for item in items_to_change:

    payload = {
        "name":item.name,
        "rarity":item.rarity,
        "item_type":item.item_type,
        "sub_type":item.sub_type
    }

    url = f'{base_url}{item_endpoint}'
    r = requests.put(url, json=payload)

    

# endpoint = "/item_info/list"

# weapons = requests.get(f'{base_url}{endpoint}')
# print(weapons.json())

# item_endpoint = "/item_info/"
# for weapon in weapons.json():
#     weapon_info = requests.get(f'{base_url}{item_endpoint}{weapon}')
#     print(weapon_info.json())