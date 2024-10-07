import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import crud, models, schemas
from database import SessionLocal, engine

def import_csv_to_db():
    # 创建数据库表
    models.Base.metadata.create_all(bind=engine)
    
    # 创建会话
    db = SessionLocal()
    
    try:
        # 检查数据库是否为空
        if db.query(models.Product).count() == 0:
            # 读取 CSV 文件
            df = pd.read_csv("Product_names_list.csv")
            
            # 将数据导入到数据库
            for _, row in df.iterrows():
                db_product = models.Product(product_name=row['Item'])
                db.add(db_product)
            
            db.commit()
            print("CSV 数据已成功导入到 SQLite 数据库。")
        else:
            print("数据库中已有数据，跳过导入过程。")
    except Exception as e:
        print(f"导入过程中发生错误：{e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    import_csv_to_db()