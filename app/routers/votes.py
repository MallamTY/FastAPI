from fastapi import HTTPException, Depends, Response, status, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, models, oauth2
from ..database import get_db


router = APIRouter(prefix="/votes", tags=["Votes"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {vote.post_id} does not exist")
    
    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id)
    found_post = vote_query.first()
    if vote.dir == 1:
        if found_post:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user has already voted on post {vote.post_id}")
        else:
            new_vote = models.Votes(post_id=vote.post_id, user_id=current_user.id)
            print(f"========================{vote.post_id}========================{current_user.id}")
            db.add(new_vote)
            db.commit()
            return {"message": "Successfully added vote"}

    if not found_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {vote.post_id} does not exist")
    vote_query.delete(synchronize_session=False)
    db.commit()
    return {"message": "Successfully deleted vote"}