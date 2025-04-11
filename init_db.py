# create_db.py
from database import Base, engine
from models import *

print("Creating database...")
Base.metadata.create_all(bind=engine)
print("Done.")
