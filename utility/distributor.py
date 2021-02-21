#from sklearn.cluster import KMeans
import numpy as np
from model.item import Item,LinkBulletMag,LinkBullets,LinkMags,Magazines,Bullets

class KMeans():

    def __init__(self, n_clusters,max_iter):

        self.n_clusters = n_clusters
        self.max_iter = max_iter

    def initialize_centroids(self, points, k):
        """returns k centroids from the initial points"""
        centroids = np.unique(points.copy())
        centroids.shape=[len(centroids),1]
        np.random.shuffle(centroids)
        return centroids[:k]
    
    def closest_centroid(self, points, centroids):
        """returns an array containing the index to the nearest centroid for each point"""
        distances = np.sqrt(((points - centroids[:, np.newaxis])**2).sum(axis=2))
        print(distances.shape)
        return np.argmin(distances, axis=0)
    
    def move_centroids(self, points, closest, centroids):
        """returns the new centroids assigned from the points closest to them"""
        return np.array([points[closest==k].mean(axis=0) for k in range(centroids.shape[0])])
    
    def fit(self, items):

        centroids = self.initialize_centroids(items, self.n_clusters) 
        print(centroids)       
        
        for i in range(self.max_iter):   
            closest = self.closest_centroid(items, centroids)
            centroids = self.move_centroids(items, closest, centroids)

        self.cluster_centers_ = centroids
        self.labels_ = closest

def assign_rarity(items, session):
    
    kmeans = KMeans(
        n_clusters=9,
        max_iter=10,
    )
    items_nominal = [item.nominal for item in items]
    items_nominal=np.array(items_nominal)
    items_nominal.shape=[len(items_nominal),1]
    # print(items_nominal)
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
        item.min = max(round (item.min*ratio),1)
    database.session.commit()

def get_bullet(mag_name, session):
    return session.query(
         Bullets
    ).filter(
         Magazines.name == mag_name,
    ).filter(
        Magazines.name == LinkBulletMag.magname
    ).filter(
        LinkBulletMag.bulletname == Bullets.name
    ).first()

def get_bullet_by_name(name,session):
    return session.query(
         Bullets
    ).filter(
        LinkBullets.bulletname == Bullets.name
    ).filter(
        LinkBullets.itemname == name
    ).first()

def get_mag(item_name,session):
    return session.query(
         Magazines
    ).filter(
        item_name == LinkMags.itemname
    ).filter(
        LinkMags.magname == Magazines.name
    ).first()

def get_item(name,session):
    return session.query(
         Item
    ).filter(
        name == Item.name
    ).first()

def distribute_mags_and_bullets(session,items):
    weapons = items.filter(Item.item_type=="ranged")
    mags_per_weapon = 5

    for weapon in weapons:
        mag = get_mag(weapon.name,session)
        if mag:
            bullet = get_bullet(mag.name, session)
            mag_to_change = get_item(mag.name,session)
            
            if mag_to_change:
                new_nominal = weapon.nominal * mags_per_weapon
                mag_to_change.nominal = new_nominal
                
            if bullet:
                bullet_to_change = get_item(bullet.name,session)
                
                if bullet_to_change:
                    new_nominal = weapon.nominal * mags_per_weapon * mag.attachcount
                    bullet_to_change.nominal = new_nominal
        else:
            bullet = get_bullet_by_name(weapon.name, session)
            new_nominal = weapon.nominal * bullet.attachcount
            bullet_to_change = get_item(bullet.name,session)
            bullet_to_change.nominal=new_nominal
    session.commit()