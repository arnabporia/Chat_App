
from sqlalchemy import  create_engine
from sqlalchemy.orm import session , sessionmaker



url = "sqlite:///./sql_app.db"

CreatedEngine = create_engine(url , connect_args={"check_same_thread" : False})
session = sessionmaker( autocommit= False ,autoflush=False , bind=CreatedEngine)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
        
    