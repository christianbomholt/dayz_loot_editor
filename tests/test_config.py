from config import ConfigManager

config = ConfigManager("config.xml")

def test_config_getters():
  print(config.get_tiers())
  assert config.get_usages() == ['Town', 'Police', 'Military', 'item4']
  assert config.get_tiers() == ['Tier1', 'Tier2', 'Tier3', 'Tier4']
  #TODO: add test of config.get_tree_heading()
  

