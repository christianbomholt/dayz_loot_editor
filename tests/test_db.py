from config import ConfigManager, INIManager
from database import Dao

ini_manger = INIManager("app.ini")
db = Dao(ini_manger.read_ini("Database", "Database_Name"))

def test_config_getters():
  assert db.search_like_name("MassBlack")[0][1] == 'MassBlackYellowMB'
  
  for item in db.fast_search_like_name("MassBlackY"):
    assert item.get("name") in ['MassBlackYellowMB']
  

