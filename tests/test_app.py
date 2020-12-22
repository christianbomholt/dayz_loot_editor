import pytest

from app import create_app, db
from model.item import User, Base

@pytest.fixture
def client():
  app = create_app()

  app.config["TESTING"] = True
  app.testing = True
  app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

  client = app.test_client()
  with app.app_context():
      db.create_all()
      Base.metadata.tables["user"].create(bind = db.engine)
      user1 = User(username="foo", password="bar")
      db.session.add(user1)
      db.session.commit()
  yield client

def test_author(client) -> None:
  rv = client.get("/user")
  assert rv.json == {"id": 1, "username": "foo"}