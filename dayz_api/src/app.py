from typing import List
from fastapi import FastAPI, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pydantic import BaseModel

Base = declarative_base()


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    rarity = Column(String(50))
    item_type = Column(String(50))
    sub_type = Column(String(50))


engine = create_engine('sqlite:///my.db')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/item_info/{item_name}")
def read_item(item_name: str):

    item_info = session.query(Item).filter_by(name=item_name).first()
    return item_info.__dict__


@app.get("/item_list")
def read_list() -> List[str]:
    items = session.query(Item.name).distinct(Item.name).all()
    items = [item[0] for item in items]
    return items


class ItemInfo(BaseModel):
    name: str
    rarity: str
    item_type: str
    sub_type: str


@app.put("/items_update/")
async def upsert_item(item: ItemInfo):

    print(item)
    print(item.name)

    exists = session.query(Item).filter(Item.name == item.name).first()
    print(exists)

    if exists:
        raise HTTPException(status_code=404, detail="Item exists")
    else:
        item_to_add = Item(name=item.name, rarity=item.rarity,
                           sub_type=item.sub_type, item_type=item.item_type)
        session.add(item_to_add)
        session.commit()
    response_json = {"code": "succes"}
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=response_json)

# item = {
#         "name": "Weapon",
#         "rarity" : "rare",
#         "item_type": "gun",
#         "sub_type": "sniper riffle"
# }

# item = Item(**item)
# session.add(item)
# session.commit()

# uvicorn app:app
