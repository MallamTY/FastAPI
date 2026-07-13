from fastapi import Body, HTTPException, Depends, Response, status, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import get_db
from ..utils import hash_password

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)
@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponseEnvelope)
async def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(payload.password)
    payload.password = hashed_password
    new_user = models.User(**payload.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "message": "User created successfully",
        "data": new_user
    }


@router.get("/{id}", response_model=schemas.UserResponseEnvelope)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id: {id} was not found")
    else:
        return {"message": "User retrieved successfully", "data": user}
