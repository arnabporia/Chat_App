
from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session
from chat.database import get_db
from chat.pydanticModel import User
from chat.databaseModel import Users
from chat.oauth2 import authentic_user

router2 = APIRouter()

#, Admin :Users = Depends(authentic_user) 

@router2.post('/admin/users')
def add_user(us : User ,  db:Session = Depends(get_db) , Admin :Users = Depends(authentic_user)  ):
    
   new_user = Users(user_name=us.user_name , password= us.password , role= us.role  )
   db.add(new_user)
   db.commit()
   db.refresh(new_user)
   
   return new_user