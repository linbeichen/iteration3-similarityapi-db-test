from sqlalchemy.orm import Session
import models, schemas

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_product_by_product_name(db: Session, name: str):
    return db.query(models.Product).filter(models.Product.product_name == name).first()

def get_products(db: Session):
    return db.query(models.Product).all()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(product_name=product.product_name)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
