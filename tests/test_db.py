from config import ConfigManager, INIManager
from database import DAO

ini_manger = INIManager("app.ini")
db = DAO(ini_manger.read_ini("Database", "Database_Name"))

def test_config_getters():
  assert db.search_by_name("MassBlack")[0][1] == 'MassBlackYellowMB'
  
  for item in db.fast_search_by_name("MassBlackY"):
    assert item.name == 'MassBlackYellowMB'
  

