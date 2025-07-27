
from .. import models,schemas
from ..database import get_db
from sqlalchemy.orm import session
from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List


router=APIRouter()


@router.get("/posts")
def get_post(db:session =Depends(get_db),response_model=List[schemas.Post]):
    # cursor.execute("""select * from posts""")
    # posts=cursor.fetchall()

    post=db.query(models.Post).all()
    return post      


@router.get("/sqlalchemy")
def test_posts(db: session = Depends(get_db)):

    post= db.query(models.Post).all()
    print(post)
    return {"data":"successful"}

# @app.post("/createpost")
# def create_post(payLoad: dict = Body(...)):
#     print(payLoad)
#     return {"new post ":f"title: {payLoad['title']} content:{payLoad['content']}"}


@router.post("/createpost",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post1(post: schemas.PostCreate, db:session = Depends(get_db)):
    # cursor.execute(""" Insert into posts (title,content,published) values (%s,%s,%s) Returning *""",
    #             (post.title,post.content,post.published))
    # new_post=cursor.fetchone()
    # conn.commit()

    #we remove this method beacuse if we have 50 column so we have to write 50 times here so we use **post dictionary
    #which auotmatically create the column and insert the value
    # new_post= models.Post(title=post.title,content=post.content,published=post.published)

    # model_dump() is a method of pydantic model which convert the pydantic model to dictionary
    #using model_dump() we can convert the pydantic model to dictionary


    new_post=models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)   # same as returning *

    return new_post


# find the post by id

@router.get("/posts/latest")
def get_latest_post():
    post=db.query(models.Post).filter(models.Post.id==id).first()
    return post




@router.get("/posts/{id}")
def get_post(id: int, db:session = Depends(get_db)):   # if user give string instead of int it will throw error so we define the type in path
    # print(type(id))

    # cursor.execute(""" select *from posts where id=%s""",(str(id),))
    # post=cursor.fetchone()
    # print(post)
    # # post=find_post(id)
    
    #     # Response.status_code=status.HTTP_404_NOT_FOUND
    #     # return{"message":"post not found"}

    post=db.query(models.Post).filter(models.Post.id==id).first()

    if not post:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} was not found")

    return post


@router.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delte_post(id:int,db:session=Depends(get_db)):

    # cursor.execute(""" delete from posts where id=%s returning*""", (str(id),))
    # deleted_post=cursor.fetchone()
    # conn.commit()

    post=db.query(models.Post).filter(models.Post.id==id)

    if post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} was not found")

    post.delete(synchronize_session=False)
    db.commit()
  
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/posts/{id}",response_model=schemas.Post)
def update_post(id:int, post:schemas.PostCreate, db:session=Depends(get_db)):
     
    #  cursor.execute("""update posts set title=%s, content=%s, published=%s where id=%s returning* """,
    #  (post.title, post.content, post.published, str(id)))
    
    #  update_post=cursor.fetchone()
    #  conn.commit()
     
    post_query=db.query(models.Post).filter(models.Post.id==id)
    existing_post=post_query.first()
    
    if existing_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found" )

    post_query.update(post.model_dump(),synchronize_session=False)
    db.commit()

    return post_query.first()