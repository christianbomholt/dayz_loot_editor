from config import ConfigManager

config = ConfigManager("config.xml")

def test_config_getters():
  print(config.get_tiers())
  assert config.get_traders() == ['Trader 1', 'Trader 2', 'Trader 3',"EXCLUDE"]
  #assert config.get_tiers() == ['Tier1', 'Tier2', 'Tier3', 'Tier4']
  #TODO: add test of config.get_tree_heading()
  

