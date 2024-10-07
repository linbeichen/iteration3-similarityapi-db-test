import pandas as pd
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

df1 = pd.read_csv("Product_names_list.csv")

print(df1)

# 添加以下代码来检查df1的结构
print("\ndf1的基本信息:")
print(df1.info())

print("\ndf1的前几行数据:")
print(df1.head())

print("\ndf1的统计摘要:")
print(df1.describe())

print("\ndf1的列名:")
print(df1.columns)

print("\ndf1的形状(行数,列数):")
print(df1.shape)

'''
with SessionLocal() as db:
    products = crud.get_products(db)
    products_list = [{"Item": p.product_name} for p in products]

print("\n从数据库读取的产品列表:")
print(products_list)

# 如果您仍然需要DataFrame,可以保留这行
df2 = pd.DataFrame(products_list)

print(df2)

# 添加以下代码来检查df1的结构
print("\ndf2的基本信息:")
print(df2.info())

print("\ndf2的前几行数据:")
print(df2.head())

print("\ndf2的统计摘要:")
print(df2.describe())

print("\ndf2的列名:")
print(df2.columns)

print("\ndf2的形状(行数,列数):")
print(df2.shape)
'''