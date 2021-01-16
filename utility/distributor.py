from config import ConfigManager
from database.dao import Dao

class Distribute():
    def Distributor(self):
        rarities = {
            "undefined": 1,
            "Legendary": 1,
            "Extremely Rare": 1.5,
            "Very Rare": 2,
            "Rare": 2.5,
            "Somewhat Rare": 3,
            "Uncommon": 5,
            "Common": 8,
            "Very Common": 12,
            "All Over The Place": 20
            }

        targetNominal = int(self.totalNumDisplayed.get())
        currentNominal = self.database.getNominal(self.gridItems)[0]
        ratio = targetNominal/currentNominal
        for item in self.gridItems:
            if self.distributorValue.get() =="Use Rarity":
                multiplier = rarities.get(item.rarity)
                item.nominal= round(item.nominal*multiplier)
            currentNominal = self.database.getNominal(self.gridItems)[0]
            ratio = targetNominal/currentNominal
            item.nominal= max(round(item.nominal*ratio),1)
        self.database.session.commit()
        self.__populate_items(self.gridItems)