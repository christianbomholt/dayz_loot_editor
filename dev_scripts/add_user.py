from config import ConfigManager, INIManager
from database import DAO
from getpass import getpass

from model.item import User, Base

ini_manger = INIManager("app.ini")
db = DAO(ini_manger.read_ini("Database", "Database_Name"))
try:
  Base.metadata.tables["user"].create(bind = db.engine)
except:
  print("Table exists")


username = getpass(prompt="User:")

user=db.session.query(User).filter_by(username=username).first()

if user:
  print("User exists - updating password")

password =getpass()

if user:
  user.password = password
  db.session.commit()
else:
  admin = User(username=username, password=password)
  db.session.add(admin)
  
db.session.commit()
db.session.close()
