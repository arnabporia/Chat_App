
from fastapi import FastAPI,WebSocket  , Depends , status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from chat.router import room , user , joinUserRoom , auth
from chat.databaseModel import Base 
from chat.database import CreatedEngine
from chat.database import get_db
from chat.databaseModel import User_Room , Users
from chat.databaseModel import JOIN_USER_ROOM




app = FastAPI()

Base.metadata.create_all(bind=CreatedEngine)
app.mount("/static", StaticFiles(directory="chat/static"), name="static")

@app.get('/')
async def get():
    return FileResponse("chat/static/index.html")

webSocketDictonery  = {}

@app.websocket('/ws/{roomName}/{users_name}')
async def websocket_endpoint( users_name : str , roomName: str , socket : WebSocket , db:Session = Depends(get_db)   ):
 
    await socket.accept()   
  
  
   #room is present or not in db
    is_room =db.query(User_Room).filter(User_Room.room_name == roomName ).first()
    if not is_room:
         await socket.close(
             code= status.WS_1008_POLICY_VIOLATION ,
             reason=f" This '{roomName}'  is not present in db"
         )
         return 
    
   #user is present or not  in db 
    is_user = db.query(Users).filter(Users.user_name == users_name).first()  
    
    if not is_user:
            await socket.close(
             code= status.WS_1008_POLICY_VIOLATION ,
             reason=f" This '{users_name}'  is not present in db"
            )
            return 
        
    
    #room name is present in dictonery
    
    room_user =  db.query(JOIN_USER_ROOM).filter( JOIN_USER_ROOM.room_id ==is_room.room_id , JOIN_USER_ROOM.userId == is_user.user_id).first()
    if not room_user:
            await socket.close(
             code= status.WS_1008_POLICY_VIOLATION ,
             reason=f" this user not in that room"
            )
            return 
    
    
    
    if roomName not in webSocketDictonery :
      webSocketDictonery[roomName] =[]
    #that websocket connection is present or not in that room 
    #if it is not append(add) that 
     

    
    if socket not in webSocketDictonery[roomName] :
        webSocketDictonery[roomName].append(socket)
    
    try:
         while True :
          data = await socket.receive_text()
          for web in webSocketDictonery[roomName] :

               await web.send_text(data)
                  
    
    except :
        webSocketDictonery[roomName].remove(socket)
    


app.include_router(room.router1)
app.include_router(user.router2)
app.include_router(joinUserRoom.router4)
app.include_router(auth.router3)
