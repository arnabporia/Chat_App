
from fastapi import FastAPI , APIRouter , Depends , HTTPException , status
from sqlalchemy.orm import Session
from chat.databaseModel import Users
from chat.database import get_db 
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from chat.pydanticModel import User
from chat.oauth2 import create_jwt_access_token

router3 = APIRouter()

@router3.post('/admin/login')
def login_process(user_credential : OAuth2PasswordRequestForm = Depends()  , db :Session = Depends(get_db) ):
    
   is_user = db.query(Users).filter(
   Users.user_name == user_credential.username,
   Users.password == user_credential.password
).first()
   
   if not is_user :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not found the user")
    
   if not is_user.role == 'admin':
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail='user is not admin')
   
   data = {
        "user_id" : is_user.user_id
    }
   
   access_token =create_jwt_access_token(data)
   
   return {
       
       'access_token' : access_token ,
       'token_type'    : 'bearer'
   }



