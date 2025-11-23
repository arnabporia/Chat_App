from sqlalchemy.orm import declarative_base
from sqlalchemy import  Column , Integer , String 
from datetime import datetime
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql import text


Base = declarative_base()


       

class User_Room(Base):
    __tablename__= "User_Rooms"
    room_id = Column(Integer , primary_key=True ) 
    room_name = Column(String , nullable=False , unique=True)
    created_at = Column(TIMESTAMP(timezone=True) ,
                        nullable=False ,
                         server_default=text('CURRENT_TIMESTAMP') )
    
class Users(Base):
    __tablename__ ="User"
    
    user_id = Column(Integer , primary_key=True , nullable= False)
    user_name = Column(String , nullable=False)
    password = Column(String , nullable=False)
    role = Column(String , nullable=False)
    created_at = Column(TIMESTAMP(timezone=True) ,
                        nullable=False ,
                         server_default=text('CURRENT_TIMESTAMP') )
    

    
class JOIN_USER_ROOM(Base):
    __tablename__ = "JOIN_USER_ROOM"
    
    join_id = Column(Integer , primary_key=True  , nullable= False)
    userId  = Column(Integer , nullable=False  )
    room_id = Column(Integer , nullable=False )
    created_at = Column(TIMESTAMP(timezone=True) ,
                        nullable=False ,
                         server_default=text('CURRENT_TIMESTAMP') )