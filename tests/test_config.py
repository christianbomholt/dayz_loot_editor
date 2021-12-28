from config import ConfigManager

config = ConfigManager("config.xml")


def test_config_getters():
    print(config.get_tiers())
    assert config.get_traders() == ['Trader 1',
                                    'Trader 2',
                                    'Trader 3',
                                    "EXCLUDE"]
