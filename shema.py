from pydantic import BaseModel, EmailStr, config, validator
from fastapi import UploadFile, HTTPException
from typing import Any
from enum import Enum

class User_login(BaseModel):
    Email: EmailStr
    Password: str
    
    
class Create_acct(BaseModel):
    Business: str
    Email: EmailStr
    Password: str

    
class Product_model(BaseModel):
    Product: str
    Company: str
    Amount: float
    Quantity: int
    Role: str
    User_id: int
    
   
    
class Update_product(BaseModel):
    Product: str
    Company: str
    Amount: float
    Quantity: int
    Role: str
    
class Token(BaseModel):
    access_token: str
    expire_date: int
    
class Tag(Enum):
    user: str = "user"
    product: str = "product"
    
class Picture(BaseModel):
    file_name: str
    content: bytes
   
    
class product_model(BaseModel): #model for the product
    title: str 
    price: float
    image: bytes
    



            


