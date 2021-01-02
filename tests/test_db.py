from config import ConfigManager, INIManager
from database import Dao
from model import Item
ini_manger = INIManager("app.ini")
# db = Dao(ini_manger.read_ini("Database", "Database_Name"))
db = Dao("test.db")

def test_config_getters():
  assert db.search_like_name("MassBlack")[0][1] == 'MassBlackYellowMB'
  
  for item in db.fast_search_like_name("MassBlackY"):
    assert item.get("name") in ['MassBlackYellowMB']


def test_set_all():
  names = ["Massppshbox",'Massppshdrum','MassPPSH41']
  cat = "W"
  bprice = "2000"
  sprice = "1000"
  exclude = 0
  rarity = "Very Rare"
   # traderCat, buyprice, sellprice, traderExclude, rarity, name
  db.setSubtypeForTrader_fast(exclude, bprice, sprice, exclude, rarity, names)

  for item in db.fast_search_like_name("Massppsh"):
    print(item.get("name"))
    assert item.get("rarity") == 'Very Rare'
    assert item.get("traderExclude") == 0
  
def test_filter():
  selected_Mods = ("Vanilla", "Mod 1", "Mod 2")
  items = db.session.query(Item).filter(Item.mod.in_ (selected_Mods)).all()
  print(set([u.__dict__["mod"] for u in items]))

  assert set([u.__dict__["mod"] for u in items]) == set(selected_Mods)
