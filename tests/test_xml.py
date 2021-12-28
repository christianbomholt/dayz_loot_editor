from xml_manager.xml_parser import XMLReader
from model import Item


def test__roundtrip():

    xml_parser = XMLReader("tests/test.xml")._get_parser()

    items = xml_parser.get_items("Normal Map")
    expected = [
        Item(
            id=None,
            name="MassGhillieSuitBoxMossy",
            nominal="200",
            min="3",
            qmin="-1",
            qmax="-1",
            restock="100",
            lifetime="12",
            usage="Military",
            tier="Tier1",
            rarity=None,
            cat_type="weapons",
            item_type=None,
            sub_type=None,
            mod=None,
            trader=None,
            dynamic_event="1",
            count_in_cargo="0",
            count_in_hoarder="0",
            count_in_map="0",
            count_in_player="0",
            buyprice=None,
            sellprice=None,
            traderExclude=None,
            traderCat=None,
            min_stock=None,
            max_stock=None,
        )
    ]
    # assert items == expected
    assert items[0].cat_type == expected[0].cat_type
    assert items[0].name == expected[0].name
    assert items[0].count_in_player == expected[0].count_in_player
