
from .. import models,schemas,utils
from ..database import get_db
from sqlalchemy.orm import session
from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List


router=APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserPost)
def create_user(user: schemas.UserCreate, db: session = Depends(get_db)):
    # Check if user with email already exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash the password before creating the user
    hashed_password = utils.hashed_password(user.password)
    user_data = user.model_dump()
    user_data["password"] = hashed_password
    
    # Create new user with the hashed password
    new_user = models.User(**user_data)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.UserPost)
def get_user(id:int, db: session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with{id}  was not found")
    return user


