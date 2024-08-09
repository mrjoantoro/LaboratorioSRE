from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db.db import SessionLocal, init_db
from src.models.models import LostProduct, ProductStatus, User
from pydantic import BaseModel
from typing import List, Optional
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from src.auth.auth import verify_password, get_password_hash, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

app = FastAPI()

init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class ProductCreate(BaseModel):
    name: str
    description: str
    location: str
    date_lost: str

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    date_lost: Optional[str] = None
    status: Optional[ProductStatus] = None

class UserCreate(BaseModel):
    username: str
    password: str

@app.post("/api/users/", response_model=dict)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"username": db_user.username, "message": "User created successfully"}

@app.post("/api/token", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

@app.post("/api/products", response_model=dict)
def create_product(product: ProductCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_product = LostProduct(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return {"id": db_product.id, "message": "Product registered successfully"}

@app.get("/api/products", response_model=List[dict])
def read_products(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(LostProduct).all()

@app.put("/api/products/{product_id}", response_model=dict)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_product = db.query(LostProduct).filter(LostProduct.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)
    db.commit()
    return {"message": "Product updated successfully"}

@app.delete("/api/products/{product_id}", response_model=dict)
def delete_product(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_product = db.query(LostProduct).filter(LostProduct.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}

@app.get("/api/products/search", response_model=List[dict])
def search_products(query: Optional[str] = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if query:
        return db.query(LostProduct).filter(LostProduct.name.ilike(f"%{query}%")).all()
    return db.query(LostProduct).all()
