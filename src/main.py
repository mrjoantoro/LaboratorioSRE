from fastapi import FastAPI
from src.api.user_routes import router as user_router
from src.api.product_routes import router as product_router

app = FastAPI()

app.include_router(user_router, prefix="/api")
app.include_router(product_router, prefix="/api")
