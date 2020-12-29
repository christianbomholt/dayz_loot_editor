from config import ConfigManager, INIManager
from database import Dao

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
  rarity = "High"
  db.setSubtypeForTrader_fast(names, cat, bprice, sprice, exclude, rarity)

  for item in db.fast_search_like_name("Massppsh"):
    print(item.get("name"))
    assert item.get("rarity") == 'High'
    assert item.get("traderExclude") == 'N'
  
  
