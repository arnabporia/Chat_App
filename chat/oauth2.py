from datetime import datetime , timedelta
from jose import jwt 
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends , HTTPException , status
from chat.databaseModel import Users
from chat.database import get_db
from sqlalchemy.orm import Session
 
oauthpassword = OAuth2PasswordBearer(tokenUrl='admin/login')

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHUM = "HS256"
ACCESSTOKEN_EXPIRE_IN_MINUTE = 30


def create_jwt_access_token(data:dict):
    copied_data =  data.copy()
    Expire_Time = datetime.utcnow() + timedelta(minutes= ACCESSTOKEN_EXPIRE_IN_MINUTE)
    copied_data.update({"exp" : Expire_Time})
    encodode_jwt =  jwt.encode(copied_data , SECRET_KEY , algorithm=ALGORITHUM)
    
    return encodode_jwt

def verify_access_token(Token : str , carendential_exception ):
    payload = jwt.decode(Token , SECRET_KEY , algorithms=[ALGORITHUM])
    
    u_id = payload.get("user_id")
    
    if not u_id :
        raise carendential_exception
    
    return u_id
    
    

def authentic_user(token: str = Depends(oauthpassword) , db: Session = Depends(get_db) ):
    
    carendential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail='Unauthrozed access')
    
    userId =verify_access_token(token , carendential_exception)
    
    USER =  db.query(Users).filter(Users.user_id == userId).first()
    
    return USER

