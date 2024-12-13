from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary, Float
from sqlalchemy.orm import relationship
from database import Base

class User_account(Base):
    __tablename__ = "user_tb"
    
    id: int = Column(Integer, primary_key=True, index=True)
    Business: str = Column(String)
    Email: str = Column(String, index=True)
    Password: str = Column(String)
    product = relationship("Product", back_populates="user_account")
    
class Product(Base):
    __tablename__ = "products"
    
    id: int = Column(Integer, primary_key=True, index=True)
    Product: str = Column(String)
    Company: str = Column(String)
    Amount: float = Column(String)
    Quantity: int = Column(String)
    Role: str = Column(String)
    user_id: int = Column(Integer, ForeignKey("user_tb.id"))
    user_account = relationship("User_account", back_populates="product")

class Test(Base): #db for the product
    __tablename__ = "file_test"
    id: int = Column(Integer, primary_key=True)
    title: str = Column(String)
    price: float = Column(Float)
    image = Column(LargeBinary)