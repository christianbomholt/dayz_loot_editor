import pyperclip
#from windows import addToClipboard
from math import ceil


rarityForTrader = {"undefined": 0,
            "Not in CE" : 0,
             "Legendary": 10,
             "Extremely Rare": 15,
             "Very Rare": 20,
             "Rare": 25,
             "Somewhat Rare": 30,
             "Uncommon": 35,
             "Common": 40,
             "Very Common": 45,
             "All Over The Place": 50}             

def getKey(item):
    return int(item[2])

def createTrader(root, subtype, rows):
    text = "\t<Category> {}\n".format(subtype)
    for row in sorted(rows, key=getKey):
        name = row[0]
        traderCat = row[1]
        buyPrice = row[2]
        sellPrice = row[3]
        excluded = True if row[4] == 1 else False
        if not excluded:
            text += "\t\t{},\t\t\t{},\t\t{},\t\t{}\n".format(name, traderCat, buyPrice, sellPrice)
    text += "\n"
    pyperclip.copy(text)

# (rarity, nominal)
def distribute(rows, minBuy, maxBuy, minSell, maxSell, useRarity):
    distribution = getDistribution(rows, useRarity)

    if len(distribution) <= 1:
        return [(minBuy, minSell) for _ in rows]

    newDist = stretch(distribution)
    buyPrices = distributePricing(newDist, maxBuy, minBuy)
    sellPrices = distributePricing(newDist, maxSell, minSell)
    buyPriceForDistrib = dict()
    sellPriceForDistrib = dict()

    for i in range(len(distribution)):
        buyPriceForDistrib[distribution[i]] = buyPrices[i]
        sellPriceForDistrib[distribution[i]] = sellPrices[i]

    buyPriceForDistrib[0] = -1
    sellPriceForDistrib[0] = -1

    return buyPriceForDistrib, sellPriceForDistrib


def getDistribution(rows, rarity_is_set):
    global rarityForTrader
    raritySet = set()

    if rarity_is_set:
        for item in rows:
            if item[0] != 0:
                raritySet.add(rarityForTrader[item[0]])
    else:
        for item in rows:
            raritySet.add(item[1])

    raritySet = sorted(raritySet)
    if 0 in raritySet and len(raritySet) > 1:
        raritySet.pop(0)
    return raritySet


def stretch(distribution):
    maxP = distribution[-1]
    minP = distribution[0]
    return scale(maxP, minP, 1, 0, distribution)


def scale(maxP, minP, newMax, newMin, todistribute):
    newPoints = []
    for point in todistribute:
        if ((maxP - minP) + newMin) != 0:
            newPoint = (point - minP)*((newMax - newMin) / (maxP - minP)) + newMin
        else:
            newPoint = 0
        newPoints.append(newPoint)
    return newPoints


def distributePricing(to_distribute, maxPrice, minPrice):

    top = to_distribute[-1] - to_distribute[0]
    bottom = 0
    pricing = []
    for point in to_distribute:
        price = (maxPrice - minPrice) * (((to_distribute[-1] - point) - bottom)**2 / (top - bottom)**2) + minPrice
        pricing.append(price)
    ouch = []

    for i in pricing:
        if i < 100:
            i = ceil(i)
        elif i < 200:
            i = ceil(i / 10) * 10
        elif i < 750:
            i = ceil(i / 25) * 25
        elif i < 1200:
            i = ceil(i / 50) * 50
        elif i < 5000:
            i = ceil(i / 100) * 100
        else:
            i = ceil(i / 500) * 500
        ouch.append(int(i))
    return ouch