from fastapi import APIRouter, Depends, status, HTTPException, Response
from ..database import get_db
from ..import schemas,oauth2,models
from sqlalchemy.orm import session
from typing import Optional

router = APIRouter(
    prefix="/votes",
    tags = ["votes"]
)

# If vote.dir == 1 (Upvote):
# If vote exists → 409 Conflict
# If no vote exists → Create new vote

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote, db:session =Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):

    post=db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id {vote.post_id} does not exist")

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id,
        models.Vote.user_id == current_user.id)

    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT,
            detail=f"current_user {current_user.id} has already voted for the post {vote.post_id}")
        
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return {"message":"vote added"}
    
    else:

        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="vote does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"vote removed"}
    