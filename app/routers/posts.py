
from typing import Optional
from fastapi import HTTPException, Depends, Response, status, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import schemas, models, oauth2
from ..database import get_db 

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=schemas.CustomPostEnvelopeList)
# @router.get("/")
async def get_posts (db: Session =  Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user), limit: int = 10, search: Optional[str] = ""):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).all()

    results = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).all()

    # print(results[0]._asdict()['Post'].title)
    return {"message": "Post retrieved successfully", "data": results}


# @app.get("/posts")
# async def get_post():
#     cursor.execute("""SELECT * FROM posts LIMIT 5""")
#     posts = cursor.fetchall()
#     return {"message": "This is the posts endpoint", "data": posts}


@router.get("/{id}", response_model=schemas.CustomPostEnvelope)
async def get_post(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)): 
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", [id])
    # post = cursor.fetchone()
    results = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    # post = db.query(models.Post).filter(models.Post.id == id) 
    if not results:
        raise HTTPException(status_code=404, detail=f"Post with id: {id} was not found")
    else:
        return {"message": "Post retrieved successfully", "data": results}

 
@router.put("/{id}", response_model=schemas.PostResponseEnvelope)
async def update_post(id: int, payload: schemas.PostCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", [payload.title, payload.content, payload.published, id])
    # updated_post = cursor.fetchone()
    # connection.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id: {id} was not found")
    else:
        if post.poster_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
        post_query.update(payload.model_dump(), synchronize_session=False)
        db.commit()
    return {"message": "Post updated successfully ", "data": post_query.first()}



@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponseEnvelope)
async def create_post(payload: schemas.PostCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                (payload.title, payload.content, payload.published))
    # new_post = cursor.fetchone()
    # connection.commit()  
    # print(**payload.model_dump())
    new_post = models.Post(poster_id=current_user.id,   **payload.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {
        "message": "Post created successfully",
        "data": new_post
        }

@router.delete("/{id}")
async def delete_post(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", [id])
    # deleted_post = cursor.fetchone()
    # connection.commit()

    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=404, detail=f"Post with id: {id} was not found")
    if post.first().poster_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    else:
        post.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=204) 