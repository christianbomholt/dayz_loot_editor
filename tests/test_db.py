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
  cat = "Category1"
  bprice = "200"
  sprice = "100"
  exclude = "N"
  rarity = "Very Rare"
  db.setSubtypeForTrader_fast(names, cat, bprice, sprice, exclude, rarity)

  for item in db.fast_search_like_name("Massppsh"):
    print(item.get("name"))
    assert item.get("rarity") == 'Very Rare'
    assert item.get("traderExclude") == "N"
  
def test_filter():
  selected_Mods = ("Vanilla", "Mod 1", "Mod 2")
  items = db.session.query(Item).filter(Item.mod.in_ (selected_Mods))
  print(set([u.__dict__["mod"] for u in items]))
  assert items == 2
