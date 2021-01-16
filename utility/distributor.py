from sklearn.cluster import KMeans
import numpy as np

def assign_rarity(items, session):

    kmeans = KMeans(
        init="random",
        n_clusters=9,
        n_init=10,
        max_iter=300,
        random_state=42
    )
    items_nominal = [item.nominal for item in items]
    items_nominal=np.array(items_nominal)
    items_nominal.shape=[len(items_nominal),1]
    
    kmeans.fit(items_nominal)
    print(kmeans.cluster_centers_)
    print(kmeans.labels_)
    labels = [sorted(kmeans.cluster_centers_).index(x) for x in kmeans.cluster_centers_]
    index  = [list(kmeans.cluster_centers_).index(x) for x in kmeans.cluster_centers_]

    mapping = dict(zip(index,labels))
    print(mapping)
    rarities = {
            0: "Legendary",
            1: "Extremely Rare",
            2: "Very Rare",
            3: "Rare",
            4: "Somewhat Rare",
            5: "Uncommon",
            6: "Common",
            7: "Very Common",
            8: "All Over The Place"
    }

    # Just for clarity
    mapped_label = [ mapping[x] for x in index]
    mapped_rarity = [ rarities[x] for x in mapped_label]
    
    print(mapped_label)
    print(mapped_rarity)

    [print(f"An item with a nominal of ~{x[0]} will have a rarity of {y}") for x,y in zip(kmeans.cluster_centers_, mapped_rarity)]

    derived_rarities = [ rarities[mapping[x]] for x in kmeans.labels_]
    
    for item, rarity in zip(items, derived_rarities):
        item.rarity = rarity

    session.commit()


def distribute_nominal(database, items, totalNumDisplayed, distributorValue):
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

    targetNominal = int(totalNumDisplayed)

    if distributorValue =="Use Rarity":

        for item in items:
                multiplier = rarities.get(item.rarity)
                item.nominal= round(item.nominal*multiplier)

    currentNominal = database.getNominal(items)[0]
    ratio = targetNominal/currentNominal
    for item in items:
        item.nominal= max(round(item.nominal*ratio),1)
    database.session.commit()
