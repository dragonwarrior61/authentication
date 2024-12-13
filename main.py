from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from passlib.context import CryptContext
from database import SessionLocal, engine, Base
from models import User_account, Product, Test
from shema import Create_acct, User_login, Product_model, Update_product, Tag, product_model, Picture
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWSError
from datetime import datetime, timedelta, timezone
from typing import Annotated
import json
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


Base.metadata.create_all(engine)

SECRET_KEY = "8671c9949fba2ff85c326f659fc5b7f0ee41ceb1ed7f33ab14838c13ce2fd7c3"
ALOGIRITHM = "HS256"
ACCESS_TOKEN = 30
 
 
 
app = FastAPI()

def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15) #utcnow()
    to_encode.update({"expr":expire.isoformat()})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALOGIRITHM)
    return encode_jwt

def decode(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALOGIRITHM])
        return payload
    except JWSError:
        return None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
pwd_password = CryptContext(schemes=["bcrypt"])
Oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")
        
@app.post("/signup", tags=[Tag.user])
async def create_account(user: Create_acct, db: Session = Depends(get_db)):
    hash_password = pwd_password.hash(user.Password)
    new_user = User_account(Business=user.Business, Email=user.Email, Password=hash_password)
    
    exits_user = db.query(User_account).filter(User_account.Email == user.Email).first()
    if exits_user:
        raise HTTPException(
            detail="alredy register",
            status_code=404
        )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login", tags=[Tag.user])
async def log_account(user: User_login, db: Session = Depends(get_db)):
    log = db.query(User_account).filter(User_account.Email == user.Email).first()
    if not log:
        raise HTTPException(
            detail="user not found",
            status_code=404
        )
    if not pwd_password.verify(user.Password, log.Password):
        raise HTTPException(
            detail="incorrect password",
            status_code=404
        )
    expire = timedelta(minutes=ACCESS_TOKEN)
    token = create_token(data={"user_id":log.id, "email":log.Email}, expires_delta=expire)
    return token


@app.post("/product", tags=[Tag.product])
async def add_product(product: Product_model, db: Session = Depends(get_db), user_id: int = 1):
    user_db = db.query(User_account).filter(User_account.id == user_id).first()
    if not user_db:
        raise HTTPException(
            status_code=404,
            detail="error id"
        )
    adder = Product(
        Product=product.Product, 
        Company=product.Company,
        Amount=product.Amount,
        Quantity=product.Quantity,
        Role=product.Role,
        user_id=user_db.id
    )
    db.add(adder)
    db.commit()
    db.refresh(adder)
    cal = product.Quantity * product.Amount
    return adder

@app.get("/get_all", tags=[Tag.product])
async def get_products(db: Session = Depends(get_db)):
    get = db.query(Product).all()
    return get

@app.delete("/delete_product/{product_id}", tags=["product"])
async def delete_item(product_id: int, db: Session = Depends(get_db)):
    item = db.query(Product).filter(Product.id == product_id).first()
    if not item:
        raise HTTPException(
            detail="product not found",
            status_code=404
        )
    db.delete(item)
    db.commit()
    return item

@app.get("/get_product/{product_id}", tags=[Tag.product])
async def get_prodcut(product_id: int, db : Session = Depends(get_db)):
    item = db.query(Product).filter(Product.id == product_id).first()
    if not item:
        raise HTTPException(
            status_code=404,
            detail="product not found"
        )
    return item

@app.put("/update_product/{product_id}", tags=[Tag.product])
async def update(product: Update_product, product_id: int, db: Session = Depends(get_db)):
    item = db.query(Product).filter(Product.id == product_id).first()
    if item is None:
        raise HTTPException(
            status_code=404,
            detail="product not found"
        )
    if product.Product is not None:
        item.Product = product.Product
        
    if product.Company is not None:
        item.Company = product.Company
        
    if product.Amount is not None:
        item.Amount = product.Amount
    
    if product.Quantity is not None:
        item.Quantity = product.Quantity
    
    if product.Role is not None:
        item.Role = product.Role
    db.commit()
    db.refresh(item)
    return item


@app.post("/new_product") #endpoint for the product
async def create_product(product: product_model, db: Session=Depends(get_db)):
    add = Test(title=product.title, price=product.price, image=product.image)
    db.add(add)
    db.commit()
    db.refresh(add)