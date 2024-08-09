from sqlalchemy import Column, Integer, String, Date, Enum, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
import enum

Base = declarative_base()

class ProductStatus(enum.Enum):
    LOST = "lost"
    FOUND = "found"
    CLAIMED = "claimed"

class LostProduct(Base):
    __tablename__ = 'lost_products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    location = Column(String, nullable=False)
    date_lost = Column(Date, nullable=False)
    status = Column(Enum(ProductStatus), default=ProductStatus.LOST)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

class ProductCreate(BaseModel):
    name: str
    description: str
    location: str
    date_lost: str  

class ProductUpdate(BaseModel):
    name: str = None
    description: str = None
    location: str = None
    date_lost: str = None
    status: ProductStatus = None
