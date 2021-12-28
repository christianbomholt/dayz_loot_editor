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

base_url = "http://localhost:8000"

endpoint = "/item_list"

weapons = requests.get(f'{base_url}{endpoint}')
print(weapons.json())

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
        session.commit()
