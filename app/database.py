"""Database & session creation."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///hw16.db', echo=True)

Session = sessionmaker(bind=engine)
session = Session()
