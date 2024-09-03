from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from fastapi import status, HTTPException, Depends, APIRouter, Response
from fastapi.security import APIKeyHeader
from ..config import settings
from typing import List


router = APIRouter(
    prefix="/itineraries",
    tags=["Itineraries"]
)


@router.get("/", response_model=List[schemas.UserItineraryOut])
def get_itinerary(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    user = db.query(models.User).filter(current_user.id == models.User.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {current_user.id} was not found")

    itineraries = db.query(models.UserItinerary).filter(current_user.id == models.UserItinerary.user_id).all()

    if not itineraries:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"This user has no itineraries.")

    return itineraries
