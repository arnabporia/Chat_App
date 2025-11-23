
from pydantic import BaseModel
from enum import Enum

class Role(str , Enum):
    user = "user" 
    admin = "admin"


class Room(BaseModel):
    room_name:str
    
class User(BaseModel):
    user_name : str
    password : str
    role : Role

class Admin(BaseModel):
    admin_name : str
    password : str
    

    
    