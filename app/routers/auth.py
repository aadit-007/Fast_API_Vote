from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import session
from ..database import get_db
from ..import schemas, utils, models,oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from passlib.context import CryptContext


router = APIRouter(tags=["Authentication"])

@router.post("/login",response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: session = Depends(get_db)):
    # Find user by email
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    # If user not found or password doesn't match, return error
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    #create token by using user id and pass it to create_acess_token function
    access_token = oauth2.create_acess_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"} 

