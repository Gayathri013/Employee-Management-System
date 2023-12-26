from database import Base , engine
from sqlalchemy import Column , Integer , String , Text , Boolean , Float
from sqlalchemy_utils import URLType


# def create_tables():
#     Base.metadata.create_all(bind = engine)

class Employees(Base):
    __tablename__ = "Employees"
    user_id = Column(String , primary_key=True , unique=True , nullable=False)
    name = Column(String, nullable=False)
    password = Column(String , nullable=False)
    email = Column(String , nullable=False , unique=True)
    age = Column(Integer)
    blood_group = Column(String)
    stack = Column(String)
    badges = Column(Integer)
    interests = Column(String)
    date_of_birth = Column(String)
    address = Column(String)
    hobbies = Column(String)
    experiance = Column(Float)
    image_url = Column(URLType)
    bravo = Column(Integer)
    raises = Column(Integer)
    trumpet = Column(Integer)
    phone_number = Column(String)
    security_q = Column(String)
    gender = Column(String)




class Admin(Base):
    __tablename__ = "Admin"
    username = Column(String , primary_key=True,unique=True  , nullable= False)
    password = Column(String , nullable=False , unique=True)


class Register(Base):
    __tablename__ = "New Employees"
    user_id = Column(String , primary_key=True , unique=True)
    name = Column(String , nullable=False)
    email = Column(String , nullable=False)
    password = Column(String , nullable=False)
    blood_group = Column(String)
    date_of_birth = Column(String)
    address = Column(String)
    security_q = Column(String)
    gender = Column(String)
    stack = Column(String)
    phone_number = Column(String)

