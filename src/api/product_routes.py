from fastapi import APIRouter, Depends
from src.services.product_service import create_product, list_products, update_product, delete_product, search_product
from src.models.product import ProductCreate, ProductUpdate

router = APIRouter()

@router.post("/products/")
async def create(product_data: ProductCreate):
    return await create_product(product_data)

@router.get("/products/")
async def read():
    return await list_products()

@router.put("/products/{product_id}")
async def update(product_id: int, product: ProductUpdate):
    return await update_product(product_id, product)

@router.delete("/products/{product_id}")
async def delete(product_id: int):
    return await delete_product(product_id)

@router.get("/products/search/")
async def search(query: str):
    return await search_product(query)
