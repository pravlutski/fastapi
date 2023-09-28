"""SQLAlchemy Data Models."""
from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.types import Integer, Float, String, DateTime
#from database import engine
from models.base import Base
from database import engine

#Base = declarative_base()


class User(Base):
    #__tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement="auto")
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())


#Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
