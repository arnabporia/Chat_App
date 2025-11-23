from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session
from chat.database import get_db
from chat.pydanticModel import Room
from chat.databaseModel import User_Room
from chat.oauth2 import authentic_user
from chat.databaseModel import Users

router1  = APIRouter()

@router1.post('/admin/room')
def create_room( room :Room , db:Session = Depends(get_db) , Admin : Users = Depends(authentic_user) ):
    
    roomcreate = User_Room(room_name = room.room_name)
    
    db.add(roomcreate)
    db.commit()
    db.refresh(roomcreate)
    
    return roomcreate

    


