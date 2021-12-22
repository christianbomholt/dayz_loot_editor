from config import ConfigManager, INIManager
from database import Dao
from model import Item
dbtest = Dao("test.db")


def test_config_getters():
    for item in dbtest.fast_search_like_name("MassBlackY"):
        assert item.get("name") in ['MassBlackYellowMB']


def test_set_all():
    names = ["Massppshbox", 'Massppshdrum', 'MassPPSH41']
    cat = "W"
    bprice = 2000
    sprice = 1000
    exclude = 0
    rarity = "Very Rare"
    # traderCat, buyprice, sellprice, traderExclude, rarity, name
    dbtest.setSubtypeForTrader_fast(
        cat, bprice, sprice, exclude, rarity, names)

    for item in dbtest.fast_search_like_name("Massppsh"):
        print(item.get("name"))
        assert item.get("rarity") == 'Very Rare'
        assert item.get("traderExclude") == 0


def test_filter():
    selected_Mods = ("Vanilla", "Mod 1", "Mod 2")
    items = dbtest.session.query(Item).filter(
        Item.mod.in_(selected_Mods)).all()
    print(set([u.__dict__["mod"] for u in items]))
    assert set([u.__dict__["mod"] for u in items]) == set(selected_Mods)
