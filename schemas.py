from pydantic import BaseModel

class ProductBase(BaseModel):
    product_name: str

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode=True


    

