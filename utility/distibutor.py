from math import ceil
from database.dao import Dao

# todo enum from rarities store at one place

rarities9 = {0: "undefined",
             50: "Legendary",
             45: "Extremely Rare",
             40: "Very Rare",
             35: "Rare",
             30: "Somewhat Rare",
             25: "Uncommon",
             20: "Common",
             15: "Very Common",
             10: "All Over The Place"}

rarityMultiplier = {50: 1, 45: 1.5, 40: 2, 35: 2.5, 30: 3, 25: 5, 20: 8, 15: 12, 10: 20}
# todo formula is not clear results are not as expected

class Dist(object):
    def __init__(self, itemsToDistribute, targetNominal, tartetMag, targetAmmo, flags):
        self.itemsToDistribute = itemsToDistribute
        self.targetNominal = targetNominal
        self.targetMag = targetMag
        self.targetAmmo = targetAmmo
        self.flags = flags

    # input: type to distribute, target nominal, targetMag, targetAmmo, List of include flags
    def distribute(itemsToDistribute, targetNominal, targetMag, targetAmmo, flags):
        itemsToDistribute = Dist.getDicts(itemsToDistribute)
        numElements = self.calculateNumElements(itemsToDistribute)
        nominalPerElement = targetNominal / numElements if numElements != 0 else 0
        setValues(nominalPerElement, itemsToDistribute)
        for item in itemsToDistribute:
            pass   

        if flags[0] == 1:
            distributeLinkedItem(itemsToDistribute, targetAmmo, "ammo")

        if flags[1] == 1:
            distributeLinkedItem(itemsToDistribute, targetMag, "mag")


    def calculateNumElements(itemsToDistribute):
        numElements = 0

        for item in itemsToDistribute:
            numElements += rarityMultiplier[item["rarity"]]
        return numElements


    def setValues(nominalPerElement, itemsToDistribute):
        for item in itemsToDistribute:
            item["nominal"] = int(round(rarityMultiplier[item["rarity"]] * nominalPerElement))
            item["min"] = int(ceil(item["nominal"] / 2))


    def distributeLinkedItem(guns, targetCount, type):
        zeroAllItems(guns, type)
        elementCount = 0
        allItems = Dao.getDicts(Dao.getType(type))
        for gun in guns:
            elementCount += int(gun["nominal"])
            linkedItemsToGun = Dao.getDicts(Dao.getWeaponAndCorresponding(gun["name"]))
            matchingItems = getLinkedOfType(linkedItemsToGun, type)

            # If Multiple item types linked: multiple Mags for example, then the sum of nominals should equal the nominal
            # of gun
            for matchingItem in matchingItems:
                for item in allItems:
                    if matchingItem["name"] == item["name"]:
                        item["nominal"] += gun["nominal"] / len(matchingItems)

        perUnit = targetCount / elementCount if elementCount != 0 else 0

        for item in allItems:
            item["nominal"] = int(ceil(item["nominal"] * perUnit))
            item["min"] = int(ceil(item["nominal"] / 2))

            Dao.update(item)


    def getLinkedOfType(linkedItems, type):
        matchingType = []
        for item in linkedItems:
            if item["type"] == type:
                matchingType.append(item)
        return matchingType


    def get_digits(string):
        return int(''.join(filter(lambda x: x.isdigit(), string)))


    def zeroAllItems(items, type):
        for item in Dist.getDicts(Dao.getItemsToZero([item["name"] for item in items], type)):
            item["nominal"] = 0
            item["min_val"] = 0

            Dao.update(item)

      