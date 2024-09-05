from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from fastapi import status, HTTPException, Depends, APIRouter, Response
from fastapi.security import APIKeyHeader
from ..config import settings


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

user_header_scheme = APIKeyHeader(name="admin_token")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), key: str = Depends(user_header_scheme)):

    if key == settings.ADMIN_TOKEN:
        try:
            hashed_password = utils.hash(user.password)
            user.password = hashed_password
            new_user = models.User(**user.model_dump())
            db.add(new_user)
            db.commit()
            db.refresh(new_user)

        except Exception:
            raise HTTPException(status_code=status.HTTP_226_IM_USED, detail=f"email or username already in use.")

        return new_user
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not authorized to perform this action")


@router.get("/", response_model=schemas.UserOut)
def get_user(current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(current_user.id == models.User.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {current_user.id} was not found")
    return user


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    user_query = db.query(models.User).filter(current_user.id == models.User.id)
    user = user_query.first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: [{current_user.id}] does not exist")

    user_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/", response_model=schemas.UserOut)
def update_user(updated_user: schemas.UserUpdate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):

    hashed_password = utils.hash(updated_user.password)
    updated_user.password = hashed_password
    user_query = db.query(models.User).filter(current_user.id == models.User.id)
    user = user_query.first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: [{current_user.id}] does not exist")

    user_query.update(updated_user.model_dump(), synchronize_session=False)
    db.commit()
    return user_query.first()


