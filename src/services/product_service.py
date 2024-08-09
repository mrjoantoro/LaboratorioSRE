from src.db.db import SessionLocal
from src.models.product import LostProduct

async def create_product(product_data):
    new_product = LostProduct(**product_data.dict())
    with SessionLocal() as db:
        db.add(new_product)
        db.commit()
        return {"id": new_product.id, "message": "Product created successfully"}

async def list_products():
    with SessionLocal() as db:
        products = db.query(LostProduct).all()
        return products

async def update_product(product_id, product_data):
    with SessionLocal() as db:
        product = db.query(LostProduct).filter(LostProduct.id == product_id).first()
        if product:
            for var, value in product_data.dict().items():
                setattr(product, var, value) if value else None
            db.commit()
            return {"message": "Product updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="Product not found")

async def delete_product(product_id):
    with SessionLocal() as db:
        product = db.query(LostProduct).filter(LostProduct.id == product_id).first()
        if product:
            db.delete(product)
            db.commit()
            return {"message": "Product deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Product not found")

async def search_product(query):
    with SessionLocal() as db:
        products = db.query(LostProduct).filter(LostProduct.name.ilike(f"%{query}%")).all()
        return products
