from xml_manager.xml_writer import XMLWriter
from database import Dao
from model import Item
dbtest = Dao("test.db")


def test__export_xml(self):
    print("DEBUG  : I am in the test function and initiated xml_writer")
    self.database = Dao("test.db")
    file = "c:/temp/test.xml"
    selected_Mods = ("Vanilla", "Mod 1", "Mod 2")

    xml_writer = XMLWriter(filename=file)
    print("DEBUG  : I am in the test function and initiated xml_writer" + file)
    items = self.database.session.query(Item).filter(
        Item.mod.in_(selected_Mods))
    xml_writer.export_xml(items, "Normal map")
