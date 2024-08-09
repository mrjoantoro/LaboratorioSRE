from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.db import SessionLocal, init_db
from src.models.models import LostProduct, ProductStatus
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ProductCreate(BaseModel):
    name: str
    description: str
    location: str
    date_lost: str

class ProductUpdate(BaseModel):
    status: ProductStatus

@app.post("/api/products", response_model=dict)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = LostProduct(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return {"id": db_product.id, "message": "Product registered successfully"}

@app.get("/api/products", response_model=List[dict])
def read_products(db: Session = Depends(get_db)):
    return db.query(LostProduct).all()

@app.put("/api/products/{product_id}", response_model=dict)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(LostProduct).filter(LostProduct.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db_product.status = product.status
    db.commit()
    return {"message": "Product updated successfully"}

@app.get("/api/products/search", response_model=List[dict])
def search_products(query: Optional[str] = None, db: Session = Depends(get_db)):
    if query:
        return db.query(LostProduct).filter(LostProduct.name.ilike(f"%{query}%")).all()
    return db.query(LostProduct).all()
