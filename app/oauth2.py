from datetime import datetime, timezone, timedelta
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from . import schemas
from .database import get_db
from . import models, schemas
from sqlalchemy.orm import session
from app.config import settings
#secretkey
#Alogorithm
#expiration time

# OAuth2PasswordBearer is a class that helps secure your API endpoints
oauth2_schema=OAuth2PasswordBearer("login")

SECRET_KEY=settings.secret_key
ALGORITHM=settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_acess_token(data: dict):
    to_encode = data.copy()   #copy the data

    expire = datetime.now(timezone.utc) + timedelta(minutes =ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    token=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return token


def verify_acccess_token(token: str, credentials_exception):
    try:
        print(f"Verifying token: {token}")
        # Add explicit expiration check
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_exp": True}
        )
        
        user_id = payload.get("user_id")
        print(f"Extracted user_id: {user_id}")
        
        if user_id is None:
            print("No user_id in token")
            raise credentials_exception
        
        # Print token expiration time
        if 'exp' in payload:
            from datetime import datetime
            exp_time = datetime.utcfromtimestamp(payload['exp'])
            print(f"Token expires at: {exp_time} (UTC)")
        
        return schemas.TokenData(id=str(user_id))
        
    except JWTError as e:
        print(f"JWT Error: {str(e)}")
        raise credentials_exception


def get_current_user(token: str = Depends(oauth2_schema), db: session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    try:
        # Verify the token
        token_data = verify_acccess_token(token, credentials_exception)
        print(f"Token verified for user_id: {token_data.id}")
        
        # Get the user from database
        user = db.query(models.User).filter(models.User.id == token_data.id).first()
        
        if user is None:
            print(f"User not found with id: {token_data.id}")
            raise credentials_exception
            
        print(f"User authenticated: {user.email}")
        return user
        
    except Exception as e:
        print(f"Authentication error: {str(e)}")
        raise credentials_exception
        
