
from .. import models,schemas,oauth2
from ..database import get_db
from sqlalchemy.orm import session
from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy import func


router=APIRouter(
    prefix="/posts",
    tags=["posts"]    # seperate the tags for post and user in swagger
)


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(
    db: session = Depends(get_db),                
    current_user: models.User = Depends(oauth2.get_current_user),
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = "",                     
):
    # Get posts with vote counts and owner information
    results = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"), models.User)
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .join(models.User, models.User.id == models.Post.owner_id)
        .group_by(models.Post.id, models.User.id)
        .filter(models.Post.title.contains(search))
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    # Format the response to match PostOut schema
    formatted_posts = []
    for post, votes, owner in results:
        post_dict = {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "published": post.published,
            "created_at": post.created_at,
            "owner_id": post.owner_id,
            "owner": {
                "id": owner.id,
                "email": owner.email
            },
            "votes": votes or 0
        }
        formatted_posts.append(post_dict)
    
    return formatted_posts


@router.post("/createpost",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post1(post: schemas.PostCreate, db:session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    print(current_user)
    post_data = post.model_dump()
    post_data['owner_id'] = current_user.id
    new_post = models.Post(**post_data)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)   # same as returning *

    return new_post


# find the post by id

@router.get("/latest", response_model=schemas.Post)
def get_latest_post(
    db: session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    user_id: Optional[int] = None
):
    query = db.query(models.Post)
    
    if user_id is not None:
        query = query.filter(models.Post.owner_id == user_id)
    
    post = query.order_by(models.Post.created_at.desc()).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No posts found"
        )
        
    return post

@router.get("/{id}",response_model=schemas.Post)
def get_post(id: int, db:session = Depends(get_db), current_user: int =Depends(oauth2.get_current_user)):   # if user give string instead of int it will throw error so we define the type in path
   
    post=db.query(models.Post).filter(models.Post.id==id).first()

    # post=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.post.id == id).first()

    if not post:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} was not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")

    return post


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} was not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")

    # post.delete(synchronize_session=False)
    db.delete(post)
    db.commit()
    return Response("data""post deleted successfully",status_code=status.HTTP_204_NO_CONTENT)



@router.put("/posts/{id}",response_model=schemas.Post)
def update_post(id:int, post:schemas.PostCreate, db:session=Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

    post_query=db.query(models.Post).filter(models.Post.id==id)
    existing_post=post_query.first()
    
    if existing_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found" )

    if existing_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")

    post_query.update(post.model_dump(),synchronize_session=False)
    db.commit()

    return post_query.first()