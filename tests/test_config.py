from config import ConfigManager

config = ConfigManager("config.xml")

expected = "Trader 1"


def test_config_getters():
    print(config.get_tiers())
    assert expected in config.get_traders()
