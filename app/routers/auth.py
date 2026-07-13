from fastapi import HTTPException, Depends, Response, status, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm 
from sqlalchemy.orm import Session
from .. import schemas, models, oauth2
from ..database import get_db
from ..utils import  verify_password
from ..oauth2 import create_access_token


router = APIRouter(
    tags=["Authentication"],
    prefix="/auth"
)


@router.post("/login", response_model=schemas.UserLoginResponse)
def login(payload: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
     user = db.query(models.User).filter(models.User.email == payload.username).first()

     if not user:
          raise  HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Invalid credentials")
     is_valid_password = verify_password(payload.password, user.password)
     if is_valid_password == False:
          raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Invalid credentials")
     
     payload = {"user_id": user.id}
     token = create_access_token(payload)
     return {"message": "Login successful", "access_token": token, "token_type": "bearer"}