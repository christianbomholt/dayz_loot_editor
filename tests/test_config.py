from config import ConfigManager

config = ConfigManager("config.xml")

def test_config_getters():
  print(config.get_tires())
  assert config.get_usages() == ['Town', 'Police', 'Military', 'item4']
  assert config.get_tires() == ['Tier1', 'Tier2', 'Tier3', 'Tier4']
  #TODO: add test of config.get_tree_heading()
  

