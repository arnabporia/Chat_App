from fastapi import APIRouter   
#from chat.pydanticModel import Join
from chat.database import get_db
from chat.databaseModel import Users , User_Room ,JOIN_USER_ROOM 
from sqlalchemy.orm import Session
from fastapi import Depends , HTTPException , status 
from chat.oauth2 import authentic_user

router4 = APIRouter()

@router4.post('/admin/users/joinRoom')
def add_Join_User_Romm(roomName : str , usersName : str , db : Session = Depends(get_db), Admin : Users = Depends(authentic_user) ):
    
    user = db.query(Users).filter(Users.user_name == usersName).first()
    
    if not user :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail='users not found')
    
    room = db.query(User_Room).filter(User_Room.room_name == roomName).first()
    
    if not room :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail='room not found')
    
     
    join_users = JOIN_USER_ROOM(userId = user.user_id , room_id = room.room_id)
    
    db.add(join_users)
    db.commit()
    db.refresh(join_users)
    
    return join_users
     
     
     
    
    