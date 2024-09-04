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


@router.post("/", response_model=schemas.UserItineraryOut)
def create_itinerary(itinerary_data: schemas.ItineraryCreate, db: Session = Depends(get_db),
                     current_user: int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(current_user.id == models.User.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {current_user.id} was not found")

    user_itinerary = models.UserItinerary(user_id=current_user.id)
    db.add(user_itinerary)
    db.commit()
    db.refresh(user_itinerary)

    itinerary = models.Itinerary(
        user_itinerary_id=user_itinerary.id,
        district_id=itinerary_data.district_id
    )
    db.add(itinerary)
    db.commit()
    db.refresh(itinerary)

    if itinerary_data.activity_id:
        # Associate Activities
        for activity_id in itinerary_data.activity_id:
            itinerary_activity = models.ItineraryActivity(
                itinerary_id=itinerary.id,
                activity_id=activity_id
            )
            db.add(itinerary_activity)

    if itinerary_data.hotels_restaurant_id:
        # Associate Hotels/Restaurants
        for hotel_restaurant_id in itinerary_data.hotels_restaurant_id:
            itinerary_hotel_restaurant = models.ItineraryHotelRestaurant(
                itinerary_id=itinerary.id,
                hotel_restaurant_id=hotel_restaurant_id
            )
            db.add(itinerary_hotel_restaurant)

    if itinerary_data.transportation_id:
        # Associate Transportations
        for transportation_id in itinerary_data.transportation_id:
            itinerary_transportation = models.ItineraryTransportation(
                itinerary_id=itinerary.id,
                transportation_id=transportation_id
            )
            db.add(itinerary_transportation)

    if itinerary_data.attraction_id:
        # Associate Attractions
        for attraction_id in itinerary_data.attraction_id:
            itinerary_attraction = models.ItineraryAttraction(
                itinerary_id=itinerary.id,
                attraction_id=attraction_id
            )
            db.add(itinerary_attraction)

    db.commit()

    return user_itinerary


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_itinerary(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(current_user.id == models.User.id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: [{current_user.id}] does not exist")

    itinerary_query = db.query(models.UserItinerary).filter(current_user.id == models.UserItinerary.user_id,
                                                            id == models.UserItinerary.id)
    itinerary = itinerary_query.first()

    if not itinerary:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Itinerary with id: [{id}] does not exist under this user.")

    itinerary_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/generate", response_model=schemas.UserItineraryOut)
def generate_itinerary():
    pass
